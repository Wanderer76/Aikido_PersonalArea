# Generated by Django 3.2.7 on 2021-10-31 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalArea', '0013_alter_request_event_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='event_name',
            new_name='event',
        ),
    ]
