import datetime
from argparse import ArgumentError

from django.db import transaction
from django.http import JsonResponse, FileResponse
from pytils.translit import slugify
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from Utilities import xls_parser
from Utilities.services import get_day_before
from events.models import Request, Events
from events.serializations import Events_ListSerializer, Events_Serializer, Requests_Serializer


class IsTrainerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer


class CreateEvent(APIView):
    """ json формат в котором нужно передавать данные
           {
           "event_name":"название мероприятия",
           "date_of_event":"дата начала семинара в формате гггг-мм-дд",
           "end_of_event":"дата конца семинара в формате гггг-мм-дд",
           "city":"город",
           "responsible_club":"ответственный клуб"
           "responsible_trainer":"фио ответственного тренера"
           }
    """

    permission_classes = (permissions.IsAdminUser,)

    @transaction.atomic
    def post(self, request):
        # data = JSONParser().parse(request.data['data'])
        # data['start_record_date'] = datetime.datetime.today()
        # data['end_record_date'] = get_day_before(datetime.date.fromisoformat(data['date_of_event']))
        # data['slug'] = slugify(data['event_name'])
        # data['poster'] = file

        serializer = Events_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['start_record_date'] = datetime.datetime.today()
            serializer.validated_data['end_record_date'] = get_day_before(
                datetime.date.fromisoformat(str(serializer.validated_data['date_of_event'])))
            serializer.validated_data['slug'] = slugify(serializer.validated_data['event_name'])
            serializer.save()

            return Response(status=status.HTTP_201_CREATED, data={'content': 'created'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class EventInfoLoad(APIView):
    """вызов api/v1/admin/seminar/download/<str:seminar_name>/ """
    permission_classes = (permissions.IsAdminUser,)
    parser_classes = (JSONParser, FileUploadParser,)

    def get(self, request, seminar_url):
        try:
            stream_file = xls_parser.createXlsxFromRequests(seminar_url)
            return FileResponse(stream_file, as_attachment=True, status=status.HTTP_200_OK)
        except ArgumentError as exception:
            return JsonResponse(data={'result': exception.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, seminar_url):
        data = request.data['file']
        try:
            result = xls_parser.parseXlsToDb(seminar_url, data)
            return Response(data={'result': result}, status=status.HTTP_200_OK)
        except ArgumentError as error:
            return Response(data={'result': error.args}, status=status.HTTP_400_BAD_REQUEST)


class CreateRequest(APIView, IsTrainerPermission):
    """json формат в котором нужно передавать данные
           [ {
          "name":"Имя",
          "surname":"Фамилия",
          "second_name":"Отчество"[не обязательно],
          "member_id": id ид участника: int[не обязательно],
          "birthdate":"дата в формате гггг-мм-дд",
          "event_name":"Название события",
          "trainer_id": ид тренера: int
          } ]"""

    permission_classes = (IsTrainerPermission,)

    @transaction.atomic
    def post(self, request):
        data = JSONParser().parse(request)
        trainer_id = data[0]['trainer_id']
        current_trainer_requests = Request.objects.prefetch_related('event').filter(event_name=data[0]['event_name'],
                                                                                    trainer_id=trainer_id)
        if current_trainer_requests.exists():
            current_trainer_requests.delete()
        serializer = Requests_Serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': 'заявка создана'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class TrainerEventRequest(APIView, IsTrainerPermission):
    permission_classes = (IsTrainerPermission,)

    def get(self, request, event_name):
        trainer_id = Token.objects.get(key=request.headers.get('Authorization')[6:]).user_id
        requests = Request.objects.filter(trainer_id=trainer_id, event_name=event_name)
        serializer = Requests_Serializer(requests, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class EventsList(APIView, IsTrainerPermission):
    """
    Возвращает данные в следующем формате
    {
    "upcoming":[
        {
        "event_name":"1",
        "date_of_event":"2021-11-30",
        "end_of_event":"2021-12-01",
        "start_record_date":"2021-11-22T16:33:24.709532Z",
        "end_record_date":"2021-11-29T23:59:59Z",
        "city":"sdf",
        "responsible_club":"sfd",
        "responsible_trainer":"sfd"
        }
    ],
    "past":[
        {
        "event_name":"название мероприятия111",
        "date_of_event":"2000-05-05",
        "end_of_event":"2021-11-20",
        "start_record_date":"2000-05-05T00:00:00Z",
        "end_record_date":"2000-05-05T00:00:00Z",
        "city":"город",
        "responsible_club":"ответственный клуб",
        "responsible_trainer":"None"
        }
    ]
    """
    permission_classes = (IsTrainerPermission,)

    @transaction.atomic
    def get(self, request):
        events = Events.objects.all()
        upcoming = Events_ListSerializer(
            events.filter(
                end_record_date__gte=datetime.date.today()).order_by('start_record_date'), many=True).data
        past = Events_ListSerializer(
            events.filter(date_of_event__lt=datetime.date.today()).order_by('start_record_date'), many=True).data

        result = {'upcoming': upcoming, 'past': past}
        return Response(status=status.HTTP_200_OK, data=result)


class EventView(APIView, IsTrainerPermission):
    permission_classes = (IsTrainerPermission,)

    def get(self, request, event_name):
        try:
            event = Events_Serializer(Events.objects.get(event_name=event_name)).data
            return JsonResponse(data={"result": event})
        except:
            return JsonResponse(data={"result": "события не существует"})
