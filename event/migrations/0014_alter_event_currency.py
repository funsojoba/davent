# Generated by Django 4.2.1 on 2023-05-25 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0013_event_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="currency",
            field=models.CharField(blank=True, default="NGN", max_length=5, null=True),
        ),
    ]
