# Generated by Django 3.2.7 on 2022-04-01 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalArea', '0005_alter_events_responsible_club'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='event_name',
            new_name='event',
        ),
    ]
