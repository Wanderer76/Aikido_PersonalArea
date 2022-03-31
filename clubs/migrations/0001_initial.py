# Generated by Django 3.2.7 on 2022-03-31 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='logo_images/')),
                ('main_trainers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_trainers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]