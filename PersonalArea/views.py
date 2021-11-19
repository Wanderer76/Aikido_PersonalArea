from ctypes import ArgumentError

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import unicode
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission

from PersonalArea.serializations import *
from PersonalArea.models import *
from Utilities import xls_parser
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
            aikiboy = Aikido_Member.objects.get(id=data['id'], password=data['password'])
            aikiToken = Token.objects.get(user=aikiboy)
            return Response(data={"token": unicode(aikiToken)}, status=status.HTTP_200_OK)
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
    def get(self, request):
        data = request.headers.get('Authorization')[6:]
        aiki_id = Token.objects.get(key=data).user_id
        aiki_ser = Profile_Serializer(Aikido_Member.objects.get(id=aiki_id)).data
        aiki_seminars = Seminar_Serializer(Seminar.objects.filter(member__id=aiki_id), many=True).data
        aiki_ser["seminars"] = aiki_seminars
        return Response(aiki_ser, status=status.HTTP_200_OK)


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
        filename = xls_parser.createXlsxFromRequests(seminar_name)
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

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)



@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        res = xls_parser.parseXlsToDb(r'C:\Users\Artyom\Desktop\test.xlsx')
        return JsonResponse(data={"result":res})
        #students = Aikido_Member.objects.all()
        #serializer = Aikido_MemberSerializer(students, many=True)
        #return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Aikido_MemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
