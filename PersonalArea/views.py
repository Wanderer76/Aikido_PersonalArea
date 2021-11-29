from ctypes import ArgumentError

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadhandler import FileUploadHandler, TemporaryFileUploadHandler
from django.db import transaction
from django.db.models import Count, QuerySet
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import unicode
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import BasePermission
from PersonalArea.serializations import *
from PersonalArea.models import *
from Utilities import xls_parser
from rest_framework.response import Response
from rest_framework.views import APIView

from Utilities.services import get_day_before


class IsTrainerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_trainer


class LoginAPIView(APIView):
    """json формат в котором нужно передавать данные
    {
        "id": int,
        "password": "password"
    }
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            aikiboy = Aikido_Member.objects.get(id=data['id'], password=data['password'])
            aikiToken = Token.objects.get(user=aikiboy)
            hasbikStatus = ""
            if aikiboy.is_admin or aikiboy.is_superuser:
                hasbikStatus = "admin"
            elif aikiboy.is_trainer:
                hasbikStatus = "trainer"
            else:
                hasbikStatus = "user"

            return Response(data={"token": unicode(aikiToken),"status":hasbikStatus}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={"error": "Неверный id или пароль"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminLoginAPIView(APIView):
    """json формат в котором нужно передавать данные
    {
        "login": "login",
        "password": "password"
    }
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            aikiboy = Aikido_Member.objects.get(login=data['login'], password=data['password'])
            if aikiboy.is_admin:
                aikiToken = Token.objects.get(user=aikiboy)
                return Response(data={"token": unicode(aikiToken)}, status=status.HTTP_200_OK)
            else:
                raise ObjectDoesNotExist()

        except ObjectDoesNotExist:
            return Response(data={"error": "Неверный id или пароль"}, status=status.HTTP_400_BAD_REQUEST)


class StudentInfo(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        data = request.headers.get('Authorization')[6:]
        aiki_id = Token.objects.get(key=data).user_id
        aiki_chel = Aikido_Member.objects.get(id=aiki_id)
        aiki_ser = Profile_Serializer(aiki_chel).data
        aiki_seminars = Seminar_Serializer(Seminar.objects.filter(member__id=aiki_id).order_by("attestation_date"), many=True).data
        aiki_ser["seminars"] = aiki_seminars

        if aiki_chel.is_trainer:
            aiki_ser["members"] = Aikido_Member.objects.filter(trainer_id=aiki_id).count()
            aiki_ser["license"] = None

        return Response(aiki_ser, status=status.HTTP_200_OK)


class TrainerHasbiks(APIView):
    def get(self, request):
        try:
            data = request.headers.get('Authorization')[6:]
            aiki_id = Token.objects.get(key=data).user_id
            aiki_chel = Aikido_Member.objects.get(id=aiki_id)

            if aiki_chel.is_trainer:
                hasbiki = Deti_Serializer(Aikido_Member.objects
                                          .filter(trainer_id=aiki_chel.id), many=True).data

                for hasbik in hasbiki:
                    seminar_boy = Seminar_Serializer(Seminar.objects
                                                     .filter(member__id=hasbik["id"]).latest())
                    hasbik["attestation_date"] = seminar_boy.data["attestation_date"]
                    hasbik["ku"] = seminar_boy.data["newKu"]

                return Response(data={"список учеников": hasbiki}, status=status.HTTP_200_OK)
            else:
                raise ObjectDoesNotExist

        except ObjectDoesNotExist:
            return Response(data={"error": "вы не тренер"}, status=status.HTTP_400_BAD_REQUEST)


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
        data = JSONParser().parse(request)
        print(data)
        data['start_record_date'] = datetime.datetime.today()
        data['end_record_date'] = get_day_before(datetime.date.fromisoformat(data['date_of_event']))
        serializer = Events_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': 'created'})
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)


class DownloadRequests(APIView):
    """вызов api/v1/seminar/<str:seminar_name>/ """
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, seminar_name):
        try:
            filename = xls_parser.createXlsxFromRequests(seminar_name)
            return FileResponse(open(filename, 'rb'),status=status.HTTP_200_OK)
        except ArgumentError:
            return JsonResponse(data={'result': 'Не существует такого мероприятия'},status=status.HTTP_400_BAD_REQUEST)


class LoadRequests(APIView):
    """вызов api/v1/seminar/<str:seminar_name>/ """
    permission_classes = (permissions.IsAdminUser,)
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format=None):
        data = request.data['file']
        with open('requests/' + filename + ".xlsx", 'wb+') as destination:
            for chunk in data.chunks():
                destination.write(chunk)
            result = xls_parser.parseXlsToDb(destination.name)
            return Response(data={'result': result})


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
        current_trainer_requests = Request.objects.filter(trainer_id=trainer_id)
        if current_trainer_requests.exists():
            current_trainer_requests.delete()
        serializer = Requests_Serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': 'заявка создана'})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)


class TrainerEventRequest(APIView, IsTrainerPermission):
    permission_classes = (IsTrainerPermission,)

    def get(self, request, event_name):
        trainer_id = Token.objects.get(key=request.headers.get('Authorization')[6:]).user_id
        requests = Request.objects.filter(trainer_id=trainer_id, event_name=event_name)
        serializer = Requests_Serializer(requests, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class EventsList(APIView,IsTrainerPermission):
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
                end_record_date__gt=datetime.date.today()).order_by('start_record_date'), many=True).data
        past = Events_ListSerializer(
            events.filter(date_of_event__lt=datetime.date.today()).order_by('start_record_date'), many=True).data

        result = {'upcoming': upcoming, 'past': past}
        return Response(status=status.HTTP_200_OK, data=result)


class SeminarStatistic(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, event_name):
        seminars = Seminar.objects.filter(name=event_name).values('oldKu', 'newKu').annotate(count=Count('oldKu'))
        return Response(status=status.HTTP_200_OK, data=seminars)


class EventView(APIView,IsTrainerPermission):
    permission_classes = (IsTrainerPermission,)

    def get(self, request, event_name):
        try:
            event = Events_Serializer(Events.objects.get(event_name=event_name)).data
            return JsonResponse(data={"result": event})
        except:
            return JsonResponse(data={"result": "события не существует"})


@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        try:
            res = xls_parser.parseXlsToDb(r'C:\Users\Artyom\Desktop\test.xlsx')
            return JsonResponse(data={"result": res})
        except ArgumentError:
            return JsonResponse(data={"result": "ошибка в заполнении таблицы"})
        # students = Aikido_Member.objects.all()
        # serializer = Aikido_MemberSerializer(students, many=True)
        # return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Aikido_MemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
