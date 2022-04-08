from rest_framework import serializers

from PersonalArea.models import Aikido_Member, Achievements


class Aikido_MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        exclude = ['password', 'photo']


class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ['id', 'name', 'surname', 'second_name', 'birthdate', 'photo', 'club', 'region']


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
