import socketio
from celery import shared_task
external_sio = socketio.RedisManager('redis://', write_only=True)


@shared_task
def send_heartbeat():
    external_sio.emit("message", data="heartbeat",
                      room="heartbeat", namespace="/heartbeat")
