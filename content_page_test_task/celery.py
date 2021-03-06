import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "content_page_test_task.settings")

app = Celery("content_page_test_task", include=["contentpage.tasks"])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = "redis://redis:6379/0"
app.conf.task_serializer = "json"

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
