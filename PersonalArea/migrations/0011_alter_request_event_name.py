# Generated by Django 3.2.7 on 2021-10-31 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalArea', '0010_alter_request_member_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='event_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='event', to='PersonalArea.events'),
        ),
    ]