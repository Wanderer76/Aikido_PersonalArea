import datetime

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
from Utilities import password_generantor, services

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
                    hasbik['club'] = hasbik['club']['name']

                return Response(data={"список учеников": hasbiki}, status=status.HTTP_200_OK)
            else:
                raise ObjectDoesNotExist

        except ObjectDoesNotExist:
            return Response(data={"error": "вы не тренер"}, status=status.HTTP_400_BAD_REQUEST)


class TrainserSet(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        try:
            trainers = Aikido_Member.objects.filter(isTrainer=True)
            serializer = Profile_Serializer(trainers, many=True)
            for i in serializer.data:
                last_achievement = Achievements.objects.filter(member__id=i['id']).order_by(
                    'attestation_date').last()
                i['ku'] = last_achievement.received_ku if last_achievement is not None else ""
                i['attestation_date'] = last_achievement.attestation_date if last_achievement is not None else ""
               # i['club'] = i['club']['name']

            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.args)


class SeminarStatistic(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, event_name):
        seminars = Achievements.objects.filter(event_name=event_name).values('received_ku').annotate(
            count=Count('received_ku'))
        return Response(status=status.HTTP_200_OK, data=seminars)


class CreateTrainer(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, id=None):

        if id is not None:
            aikided = Aikido_Member.objects.get(id=id)
            aikided.isTrainer = True
            aikided.save()
            return Response(status=status.HTTP_201_CREATED, data={'content': 'created'})

        else:
            data = JSONParser().parse(request)
            if len(data) == 8:
                club = Club.objects.get(name=data['club'])
                id = services.generate_id()
                trainer = Aikido_Member()
                trainer.id = id
                trainer.password = password_generantor.generate_password()
                trainer.name = data['name']
                trainer.surname = data['surname']
                trainer.second_name = data['second_name']
                trainer.birthdate = data['birthdate']
                trainer.city = club.city
                trainer.club = club
                trainer.isTrainer = True
                trainer.save()

                achievement = Achievements()
                achievement.event_name = data['event_name']
                achievement.attestation_date = data['attestation_date']
                achievement.received_ku = data['received_ku']
                achievement.is_child = False
                achievement.member = trainer
                achievement.save()

                return Response(status=status.HTTP_201_CREATED, data={'content': 'created'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "не все поля заполнены"})


class Modificate_Trainer(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def patch(self, request, id):
        try:
            trainer = Aikido_Member.objects.get(id=id)
        except Aikido_Member.DoesNotExist:
            return JsonResponse({'message': 'такого тренера не существует'}, status=status.HTTP_404_NOT_FOUND)

        achievement = Achievements.objects.get(member=trainer)
        aboba = {k: request.data.pop(k) for k in list(request.data.keys()) if k == 'event_name'
                 or k == 'attestation_date'
                 or k == 'received_ku'}

        serializer = Trainer_Serializer(data=request.data, instance=trainer, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer2 = Achievement_Serializer(data=aboba, instance=achievement, partial=True)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()

        return Response(status=status.HTTP_200_OK, data={'content': 'updated'})

    def delete(self, request, id):
        try:
            trainer = Aikido_Member.objects.get(id=id)
        except Aikido_Member.DoesNotExist:
            return JsonResponse({'message': 'такого тренера не существует'}, status=status.HTTP_404_NOT_FOUND)

        trainer.isTrainer = False
        trainer.save()

        return JsonResponse({'message': ' etot chelovek bolshe ne trainer !!!!!!'}, status=status.HTTP_204_NO_CONTENT)


class CandidatesToTrainer(APIView):

    def get(self, request):
        current_year = datetime.date.today()
        min_year = current_year.replace(current_year.year - 18, current_year.month, current_year.day)
        members = Aikido_Member.objects.filter(birthdate__lte=min_year, isTrainer=False)
        serializer = CandidatesToTrainerSerializer(members, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        Club.objects.get(name='Практика').delete()
        return JsonResponse(data={'asd': "asd"})
