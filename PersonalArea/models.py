import datetime

from django.db import models


# Create your models here.

class Aikido_Member(models.Model):
    id = models.IntegerField(name="id", primary_key=True, unique=True)
    password = models.CharField(name="password", max_length=25)
    name = models.CharField(name="name", max_length=15, null=False)
    surname = models.CharField(name="surname", max_length=20, null=False)
    second_name = models.CharField(name="second_name", max_length=20, null=True)
    birthdate = models.DateField(name="birthdate", null=False)
    region = models.IntegerField(name="region", null=False)
    city = models.CharField(name="city", null=False, max_length=30)
    club = models.CharField(name="club", null=False, max_length=30)
    photo = models.ImageField(name="photo", null=True)
    isTrainer = models.BooleanField(name="isTrainer", null=False)
    trainer_id = models.IntegerField(name="trainer_id", null=True)

    class Meta:
        db_table = "aikido_member"
        managed = True


class Seminar(models.Model):
    name = models.CharField(name="name", max_length=100)
    member = models.ForeignKey(Aikido_Member, on_delete=models.DO_NOTHING)
    region = models.IntegerField(name="region", null=False)
    club = models.CharField("club", max_length=30, null=False)
    trainer = models.CharField(name="trainer", null=False, max_length=100)
    city = models.CharField(name="city", null=False, max_length=30)
    attestation_date = models.DateField(name="attestation_date", null=False)
    start_date = models.DateField(name="start_date", null=False)
    oldKu = models.IntegerField("oldKu", null=True)
    newKu = models.IntegerField("newKu", null=True)
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


class Application(models.Model):
    TYPES = (
        ("0", "Seminar"),
        ("1", "Competition")
    )

    type = models.CharField(name="type", choices=TYPES, max_length=11)
    participants = models.JSONField(name="participants")

    class Meta:
        db_table = "application"
        managed = True
