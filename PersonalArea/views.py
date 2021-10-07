from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from PersonalArea.models import *
from PersonalArea.serializations import *


# Create your views here.

@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        students = Aikido_Member.objects.filter(trainer_id= 2)
        serializer = Aikido_MemberSerizlizer(students, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Aikido_MemberSerizlizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

