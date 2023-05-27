# Generated by Django 4.2.1 on 2023-05-27 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0016_alter_event_currency"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="participant_capacity",
            field=models.IntegerField(
                default=0, verbose_name="How many people can register"
            ),
        ),
    ]
