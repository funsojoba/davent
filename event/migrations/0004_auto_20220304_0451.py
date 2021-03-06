# Generated by Django 3.2.12 on 2022-03-04 04:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(choices=[('ONLINE', 'ONLINE'), ('ONSITE', 'ONSITE')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
