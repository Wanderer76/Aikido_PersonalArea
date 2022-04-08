import datetime

from rest_framework import serializers

from events.models import Events, Request


class Events_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
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
