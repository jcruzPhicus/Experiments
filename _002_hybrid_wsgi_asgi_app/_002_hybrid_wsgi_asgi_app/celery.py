from datetime import timedelta
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      '_002_hybrid_wsgi_asgi_app.settings')

app = Celery('_002_hybrid_wsgi_asgi_app', broker="redis://localhost")

app.conf.beat_schedule = {
    "heartbeat": {
        "task": "asgiwebapp.tasks.heartbeat",
        "schedule": timedelta(seconds=10),
    },
}
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
