from django.db import transaction
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from PersonalArea.serializations import *
from PersonalArea.models import *
from Utilities import XlsParser


# Create your views here.

@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        XlsParser.parseRecordsToXlc('Тестовый семинар')
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



@csrf_exempt
@transaction.atomic
def create_event(request):
    """ json формат в котором нужно передавать данные
    {
    "event_name":"название мероприятия",
    "start_record_date":"дата начала записи в формате гггг-мм-дд",
    "end_record_date":"дата конца записи в формате гггг-мм-дд",
    "date_of_event":"дата события в формате гггг-мм-дд",
    "city":"город",
    "responsible_club":"ответственный клуб"
    }"""

    if request.method == 'POST':
        data = JSONParser().parse(request)
        name = data['event_name']
        if Events.objects.filter(event_name=name).exists():
            return HttpResponse(status=409, content="Такое мероприятние уже существует")

        serializer = Events_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201, content="Мероприятие создано")
        else:
            return HttpResponse(status=500, content='Ошибка заполнения формы')
    else:
        return HttpResponse(status=400, content='Не верный метод')


@csrf_exempt
@transaction.atomic
def make_request(request):
    """json формат в котором нужно передавать данные [
    {
    "name":"Имя",
    "surname":"Фамилия",
    "second_name":"Отчество"[не обязательно],
    "member_id": id ид участника: int[не обязательно],
    "birthdate":"дата в формате гггг-мм-дд",
    "event_name":"Название события",
    "trainer_id": ид тренера: int
    }
]"""

    if request.method == 'GET':
        return HttpResponse(status=400, content='Не верный метод')

    data = JSONParser().parse(request)
    if not Events.objects.filter(event_name=data['event_name']).exists():
        return HttpResponse(status=500, content='События не существует')

    serializer = Requests_Serializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=201, content='заявка создана')
    return HttpResponse(status=400,content='Ошибка заполнения формы')

