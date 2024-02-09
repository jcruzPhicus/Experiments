

from celery import shared_task


@shared_task
def heartbeat_task(widget_id, name):
    