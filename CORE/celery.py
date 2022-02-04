from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CORE.settings")

app = Celery("CORE")
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()
