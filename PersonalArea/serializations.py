import datetime

from rest_framework import serializers

from PersonalArea.models import Aikido_Member, Achievements, Request, Events

from clubs.models import Club


class Aikido_MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        exclude = ['password', 'photo']


class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Aikido_Member
        fields = ['id', 'name', 'surname','second_name' ,'birthdate', 'photo', 'club', 'region']


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


class Events_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class Clubs_Serializer(serializers.ModelSerializer):
    slug = serializers.SlugField(default="")
    class Meta:
        model = Club
        fields = '__all__'


class Requests_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        exclude = ['id']


class Events_Serializer(serializers.ModelSerializer):
    start_record_date = datetime.datetime.today()
    end_record_date = datetime.datetime.today()
    slug = serializers.SlugField(default="")
    ''' def validate(self, attrs):
        print(attrs)

    def create(self, validated_data):
        event = Events()
        event.event_name = validated_data['event_name']
        event.date_of_event = validated_data['date_of_event']
        event.end_of_event = validated_data['end_of_event']
        event.start_record_date = datetime.datetime.today()
        event.end_record_date = get_day_before(datetime.date.fromisoformat(validated_data['date_of_event']))
        event.city = validated_data['city']
        event.responsible_club = Club.objects.get(name=validated_data['responsible_club'])
        event.slug = slugify(validated_data['event_name'])
        event.schedule = validated_data['schedule']
        event.contacts = validated_data['contacts']
        event.poster = validated_data['poster']
        return event
'''

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
