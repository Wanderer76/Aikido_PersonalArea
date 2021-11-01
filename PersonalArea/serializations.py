from PersonalArea.models import Aikido_Member, Seminar, Request, Events
from rest_framework import serializers


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
