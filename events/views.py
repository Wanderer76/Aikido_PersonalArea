from argparse import ArgumentError

from django.db import transaction
from django.http import JsonResponse, FileResponse
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from PersonalArea.models import Aikido_Member
from Utilities import xls_parser
from Utilities.services import get_day_before
from events.serializations import *


class IsTrainerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer


class CreateEvent(APIView):
    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def post(self, request):
        club = Club.objects.get(name=request.data['responsible_club'])

        request.data['responsible_club'] = club.id
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


class UpdateEvent(APIView):
    permission_classes = (permissions.AllowAny,)

    @transaction.atomic
    def patch(self, request, event_slug):
        try:
            event = Events.objects.get(slug=event_slug)
            serializer = UpdateEvents_Serializer()
            serializer.update(event, request.data)
            return Response(status=status.HTTP_200_OK)
        except Events.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteEvent(APIView):
    permission_classes = (permissions.IsAdminUser,)

    @transaction.atomic
    def delete(self, request, event_slug):
        try:
            event = Events.objects.get(slug=event_slug)
            event.delete()
            return Response(status=status.HTTP_200_OK)
        except Events.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data=e)


class EventInfoLoad(APIView):
    """?????????? api/v1/admin/seminar/download/<str:seminar_name>/ """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser, FileUploadParser,)

    def get(self, request, seminar_url):
        try:
            stream_file = xls_parser.createXlsxFromRequests(seminar_url)
            return FileResponse(stream_file, as_attachment=True, status=status.HTTP_200_OK)
        except Exception as exception:
            return JsonResponse(data={'result': exception.args}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, seminar_url):
        data = request.data['file']
        try:
            result = xls_parser.parseXlsToDb(seminar_url, data)
            return Response(data={'result': result}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(data={'result': exception.args}, status=status.HTTP_400_BAD_REQUEST)


class CreateRequest(APIView, IsTrainerPermission):
    """json ???????????? ?? ?????????????? ?????????? ???????????????????? ????????????
           [ {
          "name":"??????",
          "surname":"??????????????",
          "second_name":"????????????????"[???? ??????????????????????],
          "member_id": id ???? ??????????????????: int[???? ??????????????????????],
          "birthdate":"???????? ?? ?????????????? ????????-????-????",
          "event_name":"???????????????? ??????????????",
          "trainer_id": ???? ??????????????: int
          } ]"""

    permission_classes = (IsTrainerPermission,)

    @transaction.atomic
    def post(self, request):
        token = request.headers.get('Authorization')[6:]
        aiki_id = Token.objects.get(key=token).user_id
        trainer = Aikido_Member.objects.get(id=aiki_id)

        data = JSONParser().parse(request)
        event = Events.objects.get(event_name=data[0]['event_name'])
        current_trainer_requests = Request.objects.filter(event_name=event.id, trainer_id=trainer.id)
        if current_trainer_requests.exists():
            current_trainer_requests.delete()

        for i in data:
            i['event_name'] = event.id
            i['trainer_id'] = trainer.id

        serializer = Requests_Serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': '???????????? ??????????????'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class TrainerEventRequest(APIView, IsTrainerPermission):
    permission_classes = (IsTrainerPermission,)

    def get(self, request, event_slug):
        trainer_id = Token.objects.get(key=request.headers.get('Authorization')[6:]).user_id
        requests = Request.objects.filter(trainer_id=trainer_id,
                                          event_name=Events.objects.get(slug=event_slug).id)

        event_name = Events.objects.get(slug=event_slug).event_name
        serializer = Requests_Serializer(requests, many=True).data
        for i in serializer:
            i['event_name'] = event_name

        return Response(status=status.HTTP_200_OK, data=serializer)


class BaseInfoForTrainer(APIView):
    permission_classes = (IsTrainerPermission,)

    def get(self, request, event_slug):
        try:
            event = Events.objects.get(slug=event_slug)
            count = Request.objects.filter(event_name=event.id).count()
            result = BaseInfoForTrainer_Serializer(event).data
            result['count'] = count
            return Response(data=result, status=status.HTTP_200_OK)
        except Events.DoesNotExist as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EventsList(APIView, IsTrainerPermission):
    """
    ???????????????????? ???????????? ?? ?????????????????? ??????????????
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
        "event_name":"???????????????? ??????????????????????111",
        "date_of_event":"2000-05-05",
        "end_of_event":"2021-11-20",
        "start_record_date":"2000-05-05T00:00:00Z",
        "end_record_date":"2000-05-05T00:00:00Z",
        "city":"??????????",
        "responsible_club":"?????????????????????????? ????????",
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
                end_of_event__gte=datetime.date.today()).order_by('end_of_event'), many=True).data

        past = Events_ListSerializer(
            events.filter(end_of_event__lt=datetime.date.today()).order_by('end_of_event'), many=True).data

        for i in upcoming:
            i['responsible_club'] = i['responsible_club']['name']

        for i in past:
            i['responsible_club'] = i['responsible_club']['name']

        result = {'upcoming': upcoming, 'past': past}
        return Response(status=status.HTTP_200_OK, data=result)


class UpcomingList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        events = Events.objects.all()
        upcoming = Events_ListSerializer(
            events.filter(
                end_of_event__gte=datetime.date.today()).order_by('end_of_event'), many=True).data
        for i in upcoming:
            i['responsible_club'] = i['responsible_club']['name']
            i['poster'] = request.build_absolute_uri(i['poster'])
        return Response(data=upcoming, status=status.HTTP_200_OK)


class EventView(APIView, IsTrainerPermission):
    permission_classes = (IsTrainerPermission,)

    def get(self, request, event_slug):
        try:

            event = Events_Serializer(Events.objects.get(slug=event_slug)).data
            club = Club.objects.get(id=event['responsible_club'])
            event['responsible_club'] = club.name
            event['couch_img'] = request.build_absolute_uri(event['couch_img'])
            event['logo_img'] = request.build_absolute_uri(event['logo_img'])
            event['poster'] = request.build_absolute_uri(event['poster'])
            return JsonResponse(data={"result": event})
        except Events.DoesNotExist as e:
            return JsonResponse(data={"result": "?????????????? ???? ????????????????????"})
