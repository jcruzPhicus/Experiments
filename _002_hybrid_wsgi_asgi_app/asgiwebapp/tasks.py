

from celery import shared_task
from channels.layers import get_channel_layer, InMemoryChannelLayer
from asgiref.sync import async_to_sync
import time

channel_layer: InMemoryChannelLayer = get_channel_layer()


@shared_task
def heartbeat():
    group_name = "heartbeat"
    message = {"type": "publish", "group_name": "heartbeat", "message": time.strftime(
        '%m/%d/%Y, %H:%M:%S', time.localtime())}
    print(f"sending {message} to {group_name}")
    async_to_sync(channel_layer.group_send)(group_name, message=message)
