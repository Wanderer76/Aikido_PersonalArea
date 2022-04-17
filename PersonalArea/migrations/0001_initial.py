# Generated by Django 3.2.7 on 2022-04-15 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubs', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aikido_Member',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=25)),
                ('name', models.CharField(max_length=15)),
                ('surname', models.CharField(max_length=20)),
                ('second_name', models.CharField(max_length=20, null=True)),
                ('birthdate', models.DateField()),
                ('city', models.CharField(default='Екатеринбург', max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('isTrainer', models.BooleanField(blank=True, default=False)),
                ('is_main_trainer', models.BooleanField(blank=True, default=False)),
                ('is_superuser', models.BooleanField(blank=True, default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('trainer_id', models.IntegerField(blank=True, default=None, null=True)),
                ('club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clubs.club')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'aikido_member',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Achievements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('attestation_date', models.DateField()),
                ('received_ku', models.IntegerField(null=True)),
                ('is_child', models.BooleanField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'achievements',
                'get_latest_by': 'attestation_date',
                'managed': True,
            },
        ),
    ]
