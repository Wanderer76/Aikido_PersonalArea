# Generated by Django 3.2.7 on 2022-04-05 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_alter_club_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='logo',
            field=models.ImageField(upload_to='logo_images/'),
        ),
    ]
