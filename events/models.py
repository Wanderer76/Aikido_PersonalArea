import datetime

from django.db import models
from django.utils import timezone

from clubs.models import Club


class Events(models.Model):
    event_name = models.CharField(name="event_name", unique=True, max_length=100)
    date_of_event = models.DateField(name="date_of_event", null=False, default=datetime.date.today)
    end_of_event = models.DateField(name="end_of_event", null=False, default=datetime.date.today)
    address = models.TextField(name="address")
    coordinates = models.TextField(name="coordinates")
    start_record_date = models.DateTimeField(name="start_record_date", default=datetime.datetime.now)
    end_record_date = models.DateTimeField(name="end_record_date", default=datetime.datetime.now)
    responsible_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="responsible_club")
    responsible_trainer = models.CharField(name='responsible_trainer', max_length=60, default="None")
    max_rang = models.CharField(name="max_rang", max_length=15)
    slug = models.SlugField(name='slug', max_length=150, unique=True, null=False)
    couch_img = models.ImageField(name="couch_img", upload_to='posters/components/trainer/')
    logo_img = models.ImageField(name="logo_img", upload_to='posters/components/logo/')
    coach_offset = models.JSONField(name="coach_offset")
    logo_offset = models.JSONField(name="logo_offset")
    schedule = models.JSONField(name="schedule")
    contacts = models.JSONField(name="contacts")
    poster = models.ImageField(name="poster", upload_to='posters/')

    class Meta:
        db_table = "event"
        managed = True


class Request(models.Model):
    name = models.CharField(name="name", max_length=25, default="None")
    surname = models.CharField(name="surname", max_length=25, default="None")
    second_name = models.CharField(name="second_name", max_length=25, blank=True, default='None')
    member_id = models.IntegerField(name='member_id', null=True, blank=True)
    birthdate = models.DateField(name="birthdate", default=timezone.now)
    event_name = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='event')
    trainer_id = models.IntegerField(name="trainer_id")

    class Meta:
        db_table = "request"
        managed = True
