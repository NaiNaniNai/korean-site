import os
from celery import Celery

from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_root.settings")

app = Celery("korean_site")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete-irrelevant-online-user": {
        "task": "base.tasks.delete_irrelevant_online_user",
        "schedule": crontab(0, 0, day_of_month="1"),
    }
}
