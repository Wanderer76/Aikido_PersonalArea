# Generated by Django 3.2.7 on 2022-04-04 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_remove_club_main_trainers'),
        ('PersonalArea', '0004_aikido_member_is_main_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aikido_member',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clubs.club'),
        ),
    ]