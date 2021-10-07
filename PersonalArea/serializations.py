from PersonalArea.models import Aikido_Member
from rest_framework import serializers


class Aikido_MemberSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ['id',
                  'name',
                  'surname',
                  'second_name',
                  'birthdate',
                  'region',
                  'city',
                  'club',
                  'isTrainer',
                  'trainer_id'
                  ]
