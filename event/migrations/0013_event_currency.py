# Generated by Django 4.2.1 on 2023-05-25 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0012_event_event_url_event_rsvp"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="currency",
            field=models.CharField(default="NGN", max_length=5),
        ),
    ]
