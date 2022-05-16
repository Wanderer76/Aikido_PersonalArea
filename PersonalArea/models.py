from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from clubs.models import Club


class Aikido_Account_Manager(BaseUserManager):
    def create_user(self, **kwargs):
        user = self.model(
            id=kwargs.get('id'),
            password=kwargs.get('password'),
            name=kwargs.get('name'),
            surname=kwargs.get('surname'),
            second_name=kwargs.get("second_name"),
            birthdate=kwargs.get("birthdate"),
            city=kwargs.get("city"),
            club=Club.objects.get(id=kwargs.get("club")),
            photo=kwargs.get("photo"),
            isTrainer=kwargs.get("isTrainer"),
            trainer_id=kwargs.get("trainer_id")
        )

        user.save(using=self._db)

        return user

    def create_superuser(self, id, name, surname, second_name, birthdate, city, club, password):
        user = self.model(
            id=id,
            password=password,
            name=name,
            surname=surname,
            second_name=second_name,
            birthdate=birthdate,
            city=city,
            club=Club.objects.get(id=club),
            photo=None,
            isTrainer=True,
            is_superuser=True,
            is_staff=True
        )
        user.save(using=self._db)
        return user


class Aikido_Member(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(name="id", primary_key=True, unique=True)
    password = models.CharField(name="password", max_length=25)
    name = models.CharField(name="name", max_length=15, null=False)
    surname = models.CharField(name="surname", max_length=20, null=False)
    second_name = models.CharField(name="second_name", max_length=20, null=True)
    birthdate = models.DateField(name="birthdate", null=False)
    city = models.CharField(name="city", max_length=50, null=False,default='Екатеринбург')
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(name="photo", null=True, blank=True)
    isTrainer = models.BooleanField(name="isTrainer", null=False, default=False, blank=True)
    is_main_trainer = models.BooleanField(name="is_main_trainer", default=False, blank=True)
    is_superuser = models.BooleanField(name="is_superuser", null=False, default=False, blank=True)
    is_staff = models.BooleanField(name="is_staff", default=False)
    trainer_id = models.IntegerField(name="trainer_id", null=True, default=None, blank=True)

    class Meta:
        db_table = "aikido_member"
        managed = True

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'surname', 'second_name', 'birthdate', 'city', 'club']
    objects = Aikido_Account_Manager()

    def __str__(self):
        return f"ID: {self.id} ФИО: {self.surname} {self.name} {self.second_name}"

    @property
    def is_trainer(self):
        return self.isTrainer

    @property
    def is_admin(self):
        return self.is_staff


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Achievements(models.Model):
    event_name = models.CharField(name="event_name", max_length=100)
    member = models.ForeignKey(Aikido_Member, on_delete=models.CASCADE)
    attestation_date = models.DateField(name="attestation_date", null=False)
    received_ku = models.IntegerField(name="received_ku", null=True)
    is_child = models.BooleanField(name="is_child")

    class Meta:
        db_table = "achievements"
        managed = True
        get_latest_by = 'attestation_date'

    def __str__(self):
        return f"ФИО: {self.member} - Мероприятие: {self.event_name}"