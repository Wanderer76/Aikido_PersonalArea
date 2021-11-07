from django.db import transaction
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from PersonalArea.serializations import *
from PersonalArea.models import *
from Utilities import XlsParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView



class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Create your views here.

@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        XlsParser.parseXlcToDb(r'C:\Users\Artyom\Desktop\test.xlsx')
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


class CreateEvent(APIView):
    @transaction.atomic
    def post(self, request):
        """ json формат в котором нужно передавать данные
        {
        "event_name":"название мероприятия",
        "start_record_date":"дата начала записи в формате гггг-мм-дд",
        "end_record_date":"дата конца записи в формате гггг-мм-дд",
        "date_of_event":"дата события в формате гггг-мм-дд",
        "city":"город",
        "responsible_club":"ответственный клуб"
        }"""
        data = JSONParser().parse(request)
        serializer = Events_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': 'created'})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)


class DownloadRequests(APIView):
    def get(self, request, seminar_name):
        filename = XlsParser.createXlsxFromRequests(seminar_name)
        return FileResponse(open(filename, 'rb'))


class CreateRequest(APIView):
    @transaction.atomic
    def post(self, request):
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
        data = JSONParser().parse(request)
        serializer = Requests_Serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': 'заявка создана'})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)
