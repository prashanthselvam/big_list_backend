# django_celery/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "large_list_backend.settings")
app = Celery("large_list_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
