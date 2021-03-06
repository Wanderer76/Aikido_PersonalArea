import datetime
import json

from pytils.translit import slugify
from rest_framework import serializers

from clubs.models import Club
from clubs.serializators import ClubName_Serializer
from events.models import Events, Request


class Events_ListSerializer(serializers.ModelSerializer):
    responsible_club = ClubName_Serializer()

    class Meta:
        model = Events
        fields = ['event_name', 'date_of_event', 'end_of_event', 'address', 'responsible_club', 'slug', 'poster']


class Events_ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['event_name', 'date_of_event', 'end_of_event', 'address', 'contacts']


class Requests_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        exclude = ['id']


class BaseInfoForTrainer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['event_name', 'end_record_date', 'address', 'date_of_event', 'end_of_event']


class Events_Serializer(serializers.ModelSerializer):
    start_record_date = datetime.datetime.today()
    end_record_date = datetime.datetime.today()
    slug = serializers.SlugField(default="")

    # responsible_club = ClubName_Serializer()

    class Meta:
        model = Events
        fields = '__all__'

    def update(self, instance: Events, validated_data):
        instance.poster.delete()
        instance.logo_img.delete()
        instance.couch_img.delete()

        instance.event_name = validated_data.get('event_name', instance.event_name)
        instance.date_of_event = validated_data.get('date_of_event', instance.date_of_event)
        instance.end_of_event = validated_data.get('end_of_event', instance.end_of_event)
        instance.address = validated_data.get('address', instance.address)
        instance.coordinates = validated_data.get('coordinates', instance.coordinates)
        instance.start_record_date = instance.start_record_date
        instance.end_record_date = instance.end_record_date
        instance.responsible_club = validated_data.get('responsible_club', instance.responsible_club)
        instance.responsible_trainer = validated_data.get('responsible_trainer', instance.responsible_trainer)
        instance.max_rang = validated_data.get('max_rang', instance.max_rang)
        instance.slug = slugify(instance.event_name)
        instance.couch_img = validated_data.get('couch_img', instance.couch_img)
        instance.coach_offset = validated_data.get('coach_offset', instance.coach_offset)
        instance.logo_img = validated_data.get('logo_img', instance.logo_img)
        instance.logo_offset = validated_data.get('coach_offset', instance.logo_offset)
        instance.schedule = validated_data.get('schedule', instance.schedule)
        instance.contacts = validated_data.get('contacts', instance.contacts)
        instance.poster = validated_data.get('poster', instance.poster)
        instance.save()
        return instance


class UpdateEvents_Serializer(serializers.ModelSerializer):
    start_record_date = datetime.datetime.today()
    end_record_date = datetime.datetime.today()
    slug = serializers.SlugField(default="")

    class Meta:
        model = Events
        fields = '__all__'

    def update(self, instance: Events, validated_data):
        if validated_data.__contains__('poster') and validated_data.get('poster') != 'undefined':
            instance.poster.delete()
            instance.poster = validated_data.get('poster')

        if validated_data.__contains__('logo_img') and validated_data.get('logo_img') != 'undefined':
            instance.logo_img.delete()
            instance.logo_img = validated_data.get('logo_img')

        if validated_data.__contains__('couch_img') and validated_data.get('couch_img') != 'undefined':
            instance.couch_img.delete()
            instance.couch_img = validated_data.get('couch_img')

        instance.event_name = validated_data.get('event_name', instance.event_name)
        instance.date_of_event = validated_data.get('date_of_event', instance.date_of_event)
        instance.end_of_event = validated_data.get('end_of_event', instance.end_of_event)
        instance.address = validated_data.get('address', instance.address)
        instance.coordinates = validated_data.get('coordinates', instance.coordinates)
        instance.start_record_date = instance.start_record_date
        instance.end_record_date = instance.end_record_date
        instance.responsible_club = Club.objects.get(name=validated_data.get('responsible_club'))
        instance.responsible_trainer = validated_data.get('responsible_trainer', instance.responsible_trainer)
        instance.max_rang = validated_data.get('max_rang', instance.max_rang)
        instance.slug = slugify(instance.event_name)

        instance.coach_offset = json.loads(validated_data.get('coach_offset', instance.coach_offset))
        instance.logo_offset = json.loads(validated_data.get('coach_offset', instance.logo_offset))
        instance.schedule = json.loads(validated_data.get('schedule', instance.schedule))
        instance.contacts = json.loads(validated_data.get('contacts', instance.contacts))
        instance.save()
        return instance
