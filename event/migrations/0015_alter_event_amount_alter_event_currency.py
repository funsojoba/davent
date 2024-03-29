# Generated by Django 4.2.1 on 2023-05-25 23:29

from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0014_alter_event_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="amount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
        ),
        migrations.AlterField(
            model_name="event",
            name="currency",
            field=models.CharField(
                blank=True, default=event.models.get_currency, max_length=5, null=True
            ),
        ),
    ]
