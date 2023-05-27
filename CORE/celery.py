from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CORE.settings")

app = Celery("CORE")
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     "run-update-old-event-status-every-24-hours": {
#         "task": "task.update-old-event-status",
#         "schedule": crontab(day_of_week="0-6", hour=11, minute=00),
#     }
# }


# TODO: Send reminder to users for an event, 5 days, 3 days and 1 day togo
