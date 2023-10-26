import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fetch.settings")

app = Celery("fetch")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
