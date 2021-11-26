from PersonalArea.models import Aikido_Member, Seminar, Request, Events
from rest_framework import serializers
from django.contrib.auth import authenticate


class Aikido_MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        exclude = ['password', 'photo']


class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ['id', 'name', 'surname', 'birthdate', 'photo']


# TODO изменить в дальнейшем
class Seminar_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Seminar
        fields = ['name', 'club', 'city',
                  'attestation_date', 'oldKu',
                  'newKu', 'isChild'
                  ]


class Deti_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ['id', 'name', 'surname']


class Events_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class Requests_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class Events_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
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
            region=self.validated_data['region'],
            club=self.validated_data['club'],
            photo=self.validated_data['photo'],
            isTrainer=self.validated_data['isTrainer'],
            trainer_id=self.validated_data['trainer_id']
        )
        aikiboy.save()
        return aikiboy
