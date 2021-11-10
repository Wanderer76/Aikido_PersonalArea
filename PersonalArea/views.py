from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import unicode
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission

from PersonalArea.serializations import *
from PersonalArea.models import *
from Utilities import XlsParser
from rest_framework.response import Response
from rest_framework.views import APIView


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
            login = data['id']
            aikiboy = None
            if isinstance(login, str):
                aikiboy = Aikido_Member.objects.get(login=login, password=data['password'])
            else:
                aikiboy = Aikido_Member.objects.get(id=login, password=data['password'])
            aikiToken = Token.objects.get(user=aikiboy)
            return Response(data={"token": unicode(aikiToken)}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={"error": "Неверный id или пароль"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateEvent(APIView):
    """ json формат в котором нужно передавать данные
           {
           "event_name":"название мероприятия",
           "start_record_date":"дата начала записи в формате гггг-мм-дд",
           "end_record_date":"дата конца записи в формате гггг-мм-дд",
           "date_of_event":"дата события в формате гггг-мм-дд",
           "city":"город",
           "responsible_club":"ответственный клуб"
           }
    """
    permission_classes = (permissions.IsAdminUser,)

    @transaction.atomic
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = Events_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': 'created'})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)


class DownloadRequests(APIView):
    """вызов api/v1/seminar/<str:seminar_name>/ """
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, seminar_name):
        filename = XlsParser.createXlsxFromRequests(seminar_name)
        return FileResponse(open(filename, 'rb'))


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

    permission_classes = [permissions.IsAdminUser, IsTrainerPermission]

    @transaction.atomic
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = Requests_Serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': 'заявка создана'})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)


@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        # XlsParser.parseXlcToDb(r'C:\Users\Artyom\Desktop\test.xlsx')
        students = Aikido_Member.objects.all()
        serializer = Aikido_MemberSerizlizer(students, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Aikido_MemberSerizlizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def student_seminars(request, pk):
    if request.method == 'GET':
        try:
            seminars = Seminar.objects.filter(student_id=pk)
            print(seminars.values())
        except:
            return HttpResponse(status=404)
        serializer = Seminar_Serializer(seminars, many=True)
        return JsonResponse(serializer.data, safe=False)
