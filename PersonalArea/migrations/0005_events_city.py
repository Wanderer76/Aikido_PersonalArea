# Generated by Django 3.2.7 on 2021-10-30 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalArea', '0004_auto_20211030_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='city',
            field=models.CharField(default='None', max_length=30),
        ),
    ]
