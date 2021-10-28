from PersonalArea.models import Aikido_Member, Seminar
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
                  'club',
                  'isTrainer',
                  'trainer_id',
                  ]


class Aikido_SeminarsSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Seminar
        fields = ['member','region', 'club',
                  'trainer', 'city',
                  'attestation_date', 'oldKu',
                  'newKu', 'isChild', 'examiner'
                  ]
