from rest_framework import serializers

from PersonalArea.models import Aikido_Member, Achievements
from clubs.serializators import ClubName_Serializer


class Aikido_MemberSerializer(serializers.ModelSerializer):
    club = ClubName_Serializer()

    class Meta:
        model = Aikido_Member
        exclude = ['password', 'photo']


class Profile_Serializer(serializers.ModelSerializer):
    club = ClubName_Serializer()
    class Meta:
        model = Aikido_Member
        fields = ['id', 'name', 'surname', 'second_name', 'birthdate', 'photo', 'club', 'city']


class Trainer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ('name', 'surname', 'second_name', 'birthdate', 'club')

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.surname = validated_data.get("surname", instance.surname)
        instance.second_name = validated_data.get("second_name", instance.second_name)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)
        instance.club = validated_data.get("club", instance.club)
        instance.save()
        return instance


class Achievement_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = ['event_name', 'attestation_date', 'received_ku']

    def update(self, instance, validated_data):
        instance.event_name = validated_data.get("event_name", instance.event_name)
        instance.attestation_date = validated_data.get("attestation_date", instance.attestation_date)
        instance.received_ku = validated_data.get("received_ku", instance.received_ku)
        instance.save()
        return instance


class CandidatesToTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ['id', 'name', 'surname', 'second_name']


# TODO изменить в дальнейшем
class Achievements_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = ['event_name',
                  'attestation_date', 'received_ku', 'is_child']


class Deti_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ['id', 'password', 'name', 'surname', 'birthdate']


class Member_InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ['id', 'password', 'name', 'surname', 'birthdate']


class RegistrationSerializer(serializers.ModelSerializer):
    #club = ClubName_Serializer()
    class Meta:
        model = Aikido_Member
        fields = '__all__'

    def save(self):
        aikiboy = Aikido_Member(
            id=self.validated_data['id'],
            password=self.validated_data['password'],
            name=self.validated_data['name'],
            surname=self.validated_data['surname'],
            second_name=self.validated_data['second_name'],
            birthdate=self.validated_data['birthdate'],
            city=self.validated_data['city'],
            club=self.validated_data['club'],
            photo=self.validated_data['photo'],
            isTrainer=self.validated_data['isTrainer'],
            trainer_id=self.validated_data['trainer_id']
        )
        aikiboy.save()
        return aikiboy
