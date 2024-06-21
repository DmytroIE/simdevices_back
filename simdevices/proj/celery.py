import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
app = Celery("simdevices")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# python -m celery -A proj.celery worker
# celery -A proj.celery beat -l info