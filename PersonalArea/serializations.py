from PersonalArea.models import Aikido_Member, Seminar, Request, Events
from rest_framework import serializers
from django.contrib.auth import authenticate


class Aikido_MemberSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        exclude = ['password', 'photo']


# TODO изменить в дальнейшем
class Seminar_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Seminar
        fields = ['member', 'region', 'club',
                  'trainer', 'city',
                  'attestation_date', 'oldKu',
                  'newKu', 'isChild', 'examiner'
                  ]


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
            id = self.validated_data['id'],
            password = self.validated_data['password'],
            name = self.validated_data['name'],
            surname = self.validated_data['surname'],
            second_name = self.validated_data['second_name'],
            birthdate = self.validated_data['birthdate'],
            region = self.validated_data['region'],
            club = self.validated_data['club'],
            photo = self.validated_data['photo'],
            isTrainer = self.validated_data['isTrainer'],
            trainer_id = self.validated_data['trainer_id']
        )
        aikiboy.save()
        return aikiboy

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(max_length=12, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        password = data.get('password', None)

        if password is None:
            raise serializers.ValidationError(
                'Введите пароль, чтобы авторизоваться'
            )

        user = authenticate(username=id, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким id и паролем не найден'
            )

        return {
            'id': user.id,
            'token': user.token
        }

