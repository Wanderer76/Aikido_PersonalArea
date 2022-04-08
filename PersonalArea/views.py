from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.template.defaultfilters import slugify
# from django.utils.text import slugify
# from pytils.translit import slugify
from pytz import unicode
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from PersonalArea.models import *
from PersonalArea.serializations import *


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

            return Response(data={"token": unicode(aikiToken), "status": hasbikStatus}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={"error": "Неверный id или пароль"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AikidoMembersInfo(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        aiki_info = Member_InfoSerializer(Aikido_Member.objects.all(), many=True).data
        return Response({"список учеников": aiki_info}, status=status.HTTP_200_OK)


class StudentInfo(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = request.headers.get('Authorization')[6:]
        aiki_id = Token.objects.get(key=data).user_id
        aiki_chel = Aikido_Member.objects.get(id=aiki_id)
        aiki_ser = Profile_Serializer(aiki_chel).data
        aiki_seminars = Achievements_Serializer(
            Achievements.objects.filter(member__id=aiki_id, received_ku__isnull=False).order_by("attestation_date"),
            many=True).data
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
                    seminar_boy = Achievements_Serializer(Achievements.objects
                                                          .filter(member__id=hasbik["id"],
                                                                  received_ku__isnull=False).latest())
                    hasbik["attestation_date"] = seminar_boy.data["attestation_date"]
                    hasbik["ku"] = seminar_boy.data["received_ku"]

                return Response(data={"список учеников": hasbiki}, status=status.HTTP_200_OK)
            else:
                raise ObjectDoesNotExist

        except ObjectDoesNotExist:
            return Response(data={"error": "вы не тренер"}, status=status.HTTP_400_BAD_REQUEST)






class SeminarStatistic(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, event_name):
        seminars = Achievements.objects.filter(event_name=event_name).values('received_ku').annotate(
            count=Count('received_ku'))
        return Response(status=status.HTTP_200_OK, data=seminars)



@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        Club.objects.get(name='Практика').delete()
        return JsonResponse(data={'asd':"asd"})
