# Generated by Django 3.2.7 on 2021-10-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalArea', '0007_request_birthdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='type',
        ),
        migrations.AddField(
            model_name='events',
            name='responsible_club',
            field=models.CharField(default='None', max_length=30),
        ),
    ]
