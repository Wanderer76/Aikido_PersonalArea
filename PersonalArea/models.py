import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
from django.utils import timezone

class Aikido_Account_Manager(BaseUserManager):
    def create_user(self, **kwargs):
        user = self.model(
        id = kwargs.get('id'),
        password = kwargs.get('password'),
        name = kwargs.get('name'),
        surname = kwargs.get('surname'),
        second_name = kwargs.get("second_name"),
        birthdate = kwargs.get("birthdate"),
        region = kwargs.get("region"),
        club = kwargs.get("club"),
        photo = kwargs.get("photo"),
        isTrainer = kwargs.get("isTrainer"),
        trainer_id = kwargs.get("trainer_id")
        )

        #user.set_password(kwargs.get('password'))

        user.save(using=self._db)


        return user

    def create_superuser(self, username, password):
        pass

class Aikido_Member(AbstractBaseUser):
    id = models.IntegerField(name="id", primary_key=True, unique=True)
    password = models.CharField(name="password", max_length=25)
    name = models.CharField(name="name", max_length=15, null=False)
    surname = models.CharField(name="surname", max_length=20, null=False)
    second_name = models.CharField(name="second_name", max_length=20, null=True)
    birthdate = models.DateField(name="birthdate", null=False)
    region = models.IntegerField(name="region", null=False)
    club = models.CharField(name="club", null=False, max_length=30)
    photo = models.ImageField(name="photo", null=True, blank=True)
    isTrainer = models.BooleanField(name="isTrainer", null=False, default=False, blank=True)
    trainer_id = models.IntegerField(name="trainer_id", null=True, default=None, blank=True)

    class Meta:
        db_table = "aikido_member"
        managed = True

    USERNAME_FIELD = 'id'
    REQUIRED_FIELD = '__all__'

    objects = Aikido_Account_Manager()

    def __str__(self):
        return str(id)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Seminar(models.Model):
    name = models.CharField(name="name", max_length=100)
    member = models.ForeignKey(Aikido_Member, on_delete=models.DO_NOTHING)
    club = models.CharField("club", max_length=30, null=False)
    trainer = models.CharField(name="trainer", null=False, max_length=100)
    city = models.CharField(name="city", null=False, max_length=30)
    attestation_date = models.DateField(name="attestation_date", null=False)
    start_date = models.DateField(name="start_date", null=False)
    oldKu = models.IntegerField("oldKu", null=True)
    newKu = models.IntegerField("newKu", null=True, default=None, blank=True)
    isChild = models.BooleanField("isChild", null=False)
    examiner = models.CharField("examiner", null=False, max_length=100)

    class Meta:
        db_table = "seminar"
        managed = True


class Competition(models.Model):
    name = models.CharField(primary_key=True, name="name", max_length=100, unique=True, default="unable")
    member_id = models.ForeignKey(Aikido_Member, on_delete=models.DO_NOTHING)
    region = models.IntegerField(name="region", null=False)
    club = models.CharField("club", max_length=30, null=False)
    trainer = models.CharField(name="trainer", null=False, max_length=100)
    city = models.CharField(name="city", null=False, max_length=30)
    position = models.IntegerField(name="position", null=False)

    class Meta:
        db_table = "competition"
        managed = True


class Events(models.Model):
    event_name = models.CharField(name="event_name", primary_key=True, max_length=100)
    start_record_date = models.DateField(name="start_record_date", default=datetime.date.today)
    end_record_date = models.DateField(name="end_record_date", default=datetime.date.today)
    date_of_event = models.DateField(name="date_of_event", default=datetime.date.today)
    city = models.CharField(name="city", null=False, max_length=30, default="None")
    responsible_club = models.CharField(name='responsible_club', max_length=30, default="None")

    class Meta:
        db_table = "event"
        managed = True


class Request(models.Model):
    name = models.CharField(name="name", max_length=25, default="None")
    surname = models.CharField(name="surname", max_length=25, default="None")
    second_name = models.CharField(name="second_name", max_length=25, blank=True, default='None')
    member_id = models.IntegerField(name='member_id', null=True, blank=True)
    birthdate = models.DateField(name="birthdate", default=timezone.now)
    event_name = models.ForeignKey(Events, on_delete=models.DO_NOTHING,related_name='event')
    trainer_id = models.IntegerField(name="trainer_id")

    class Meta:
        db_table = "request"
        managed = True
