from django.db import models


# Create your models here.

class User(models.Model):
    id = models.IntegerField(name="id", primary_key=True, unique=True, editable=False)
    password = models.CharField(name="password", max_length=25, primary_key=False)

    class Meta:
        managed = True
        db_table = 'users'


class Aikido_Trainer(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, name="id", primary_key=True, )
    name = models.CharField(name="name", max_length=15, null=False)
    surname = models.CharField(name="surname", max_length=20, null=False)
    second_name = models.CharField(name="second_name", max_length=20, null=True)
    birthdate = models.DateField(name="birthdate", null=False)
    region = models.IntegerField(name="region", null=False)
    city = models.CharField(name="city", null=False, max_length=30)
    club = models.CharField(name="club", null=False, max_length=30)
    belt = models.IntegerField(name="belt")
    photo = models.ImageField(name="photo")
    pass


class Aikido_Student(models.Model):
    id = models.OneToOneField(User, on_delete=models.deletion.CASCADE, primary_key=True, name="id")
    name = models.CharField(name="name", max_length=15, null=False)
    surname = models.CharField(name="surname", max_length=20, null=False)
    second_name = models.CharField(name="second_name", max_length=20, null=True)
    birthdate = models.DateField(name="birthdate", null=False)
    region = models.IntegerField(name="region", null=False)
    city = models.CharField(name="city", null=False, max_length=30)
    club = models.CharField(name="club", null=False, max_length=30)
    photo = models.ImageField(name="photo")

    isTrainer = models.BooleanField("isTrainer", null=False)
    belt = models.IntegerField(name="belt", null=True)
    trainer = models.ForeignKey(Aikido_Trainer, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = "aikido_students"
        managed = True


class Seminar(models.Model):
    student_id = models.ForeignKey(Aikido_Student, on_delete=models.DO_NOTHING)
    region = models.IntegerField(name="region", null=False)
    club = models.CharField("club", max_length=30, null=False)
    trainer = models.CharField(name="trainer", null=False)
    city = models.CharField(name="city", null=False)
    attestation_date = models.DateField(name="attestation_date", null=False)
    oldKu = models.IntegerField("oldKu", null=True)
    newKu = models.IntegerField("newKu", null=True)
    isChild = models.BooleanField("isChild", null=False)
    examiner = models.CharField("examiner", null=False)

    class Meta:
        db_table = "seminars"
        managed = True


class Competition(models.Model):
    student_id = models.ForeignKey(Aikido_Student, on_delete=models.DO_NOTHING)
    region = models.IntegerField(name="region", null=False)
    club = models.CharField("club", max_length=30, null=False)
    trainer = models.CharField(name="trainer", null=False)
    city = models.CharField(name="city", null=False)
    position = models.IntegerField(name="position", null=False)

    class Meta:
        db_table = "competitions"
        managed = True


class Application(models.Model):
    TYPES = (
        "Seminar",
        "Competition"
    )

    type = models.CharField(name="type", choices=TYPES)
    participants = models.JSONField(name="participants")

    class Meta:
        db_table = "applications"
        managed = True
