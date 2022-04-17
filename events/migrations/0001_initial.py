# Generated by Django 3.2.7 on 2022-04-08 12:08

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubs', '0004_alter_club_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('event_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('date_of_event', models.DateField(default=datetime.date.today)),
                ('end_of_event', models.DateField(default=datetime.date.today)),
                ('address', models.TextField()),
                ('coordinates', models.TextField()),
                ('start_record_date', models.DateTimeField(default=datetime.datetime.now)),
                ('end_record_date', models.DateTimeField(default=datetime.datetime.now)),
                ('responsible_trainer', models.CharField(default='None', max_length=60)),
                ('max_rang', models.CharField(max_length=15)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('couch_img', models.ImageField(upload_to='posters/components/trainer/')),
                ('logo_img', models.ImageField(upload_to='posters/components/logo/')),
                ('coach_offset', models.JSONField()),
                ('logo_offset', models.JSONField()),
                ('schedule', models.JSONField()),
                ('contacts', models.JSONField()),
                ('poster', models.ImageField(upload_to='posters/')),
                ('responsible_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsible_club', to='clubs.club')),
            ],
            options={
                'db_table': 'event',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=25)),
                ('surname', models.CharField(default='None', max_length=25)),
                ('second_name', models.CharField(blank=True, default='None', max_length=25)),
                ('member_id', models.IntegerField(blank=True, null=True)),
                ('birthdate', models.DateField(default=django.utils.timezone.now)),
                ('trainer_id', models.IntegerField()),
                ('event_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='events.events')),
            ],
            options={
                'db_table': 'request',
                'managed': True,
            },
        ),
    ]
