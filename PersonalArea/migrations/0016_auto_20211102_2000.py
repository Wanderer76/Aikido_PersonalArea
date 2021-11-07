# Generated by Django 3.2.7 on 2021-11-02 15:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalArea', '0015_rename_event_request_event_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='date_of_event',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='events',
            name='end_record_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='events',
            name='start_record_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
