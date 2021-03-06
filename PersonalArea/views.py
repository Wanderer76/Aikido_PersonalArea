import datetime
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import unicode
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from PersonalArea.models import *
from PersonalArea.serializations import *
from Utilities import password_generantor, services
from events.models import Events
from events.serializations import Events_ProfileSerializer


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
        aiki_ser["club"] = aiki_ser["club"]["name"]

        ku = None
        if aiki_seminars.__len__() > 0:
            aiki_ser["seminar_name"] = aiki_seminars[-1]["event_name"]
            aiki_ser["seminar_date"] = aiki_seminars[-1]["attestation_date"]
            ku = aiki_seminars[-1]["received_ku"]
            aiki_ser["received_ku"] = ku

            if ku == 1:
                ku = 10
            aiki_ser["next_ku"] = ku + 1 if ku > 9 else ku - 1
            months = datetime.strptime(aiki_seminars[-1]["attestation_date"],
                                       "%Y-%m-%d") + relativedelta(months=12 if ku > 9 else 6)
        else:
            aiki_ser["received_ku"] = ku
            aiki_ser["next_ku"] = 5
            aiki_sem = Achievements_Serializer(
                Achievements.objects.filter(member__id=aiki_id, received_ku__isnull=True).order_by('-attestation_date'),
                many=True).data
            aiki_ser["seminar_name"] = aiki_sem[0]["event_name"]
            aiki_ser["seminar_date"] = aiki_sem[0]["attestation_date"]
            months = datetime.strptime(aiki_sem[0]["attestation_date"],
                                       "%Y-%m-%d") + relativedelta(months=6)

        aiki_ser["next_seminar_date"] = str(months)[:10]

        if aiki_chel.is_trainer:
            aiki_ser["members"] = Aikido_Member.objects.filter(trainer_id=aiki_id).count()
            aiki_ser["area"] = aiki_chel.club.area

        achivs = Achievements_Serializer(
            Achievements.objects.filter(member__id=aiki_id).order_by("attestation_date"),
            many=True).data

        evens_names = list(item.get('event_name') for item in achivs)
        eve = Events_ProfileSerializer(Events.objects.filter(event_name__in=evens_names).order_by("date_of_event"),
                                       many=True).data

        aiki_ser["events"] = eve

        return Response(aiki_ser, status=status.HTTP_200_OK)


class TrainerHasbiks(APIView):
    def get(self, request):
        try:
            data = request.headers.get('Authorization')[6:]
            aiki_id = Token.objects.get(key=data).user_id
            aiki_chel = Aikido_Member.objects.get(id=aiki_id)
            if aiki_chel.is_trainer:
                hasbiki = Deti_Serializer(Aikido_Member.objects
                                          .filter(trainer_id=aiki_chel.id).order_by("surname"), many=True).data

                for hasbik in hasbiki:
                    achievements = Achievements.objects.filter(member=hasbik["id"],
                                                               received_ku__isnull=False)
                    if achievements.count() != 0:
                        seminar_boy = Achievements_Serializer(achievements.latest())
                        hasbik["attestation_date"] = seminar_boy.data["attestation_date"]
                        hasbik["ku"] = seminar_boy.data["received_ku"]

                return Response(data={"список учеников": hasbiki}, status=status.HTTP_200_OK)
            else:
                raise ObjectDoesNotExist

        except ObjectDoesNotExist:
            return Response(data={"error": "вы не тренер"}, status=status.HTTP_400_BAD_REQUEST)


class TrainserSet(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        try:
            trainers = Aikido_Member.objects.filter(isTrainer=True).order_by("surname")
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

        club = Club.objects.get(name=request.data['club'])
        request.data['club'] = club.id

        if trainer.is_superuser:
            if not Achievements.objects.filter(member=trainer).exists():
                if 'event_name' and 'attestation_date' and 'received_ku' in request.data.keys():
                    achievement = Achievements()
                    achievement.event_name = request.data['event_name']
                    achievement.attestation_date = request.data['attestation_date']
                    achievement.received_ku = request.data['received_ku']
                    achievement.is_child = False
                    achievement.member = trainer
                    achievement.save()
                else:
                    return JsonResponse({'message': 'заполните все поля о мероприятии аттестации'},
                                        status=status.HTTP_400_BAD_REQUEST)

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
        current_year = date.today()
        min_year = current_year.replace(current_year.year - 18, current_year.month, current_year.day)
        members = Aikido_Member.objects.filter(birthdate__lte=min_year, isTrainer=False).order_by("surname")
        serializer = CandidatesToTrainerSerializer(members, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TrainerBaseInfo(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, id):
        trainer = Aikido_Member.objects.get(id=id)
        if not trainer.isTrainer:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        first_achievment = Achievements.objects.filter(member=trainer).order_by('attestation_date').first()
        trainer_ser = Trainer_Serializer(trainer).data
        trainer_ser['club'] = Club.objects.get(id=trainer_ser['club']).name
        achievement_ser = Achievement_Serializer(first_achievment).data
        trainer_ser.update(achievement_ser)
        return Response(data=trainer_ser, status=status.HTTP_200_OK)


@csrf_exempt
def aikido_students_list(request):
    if request.method == 'GET':
        Club.objects.get(name='Практика').delete()
        return JsonResponse(data={'asd': "asd"})
