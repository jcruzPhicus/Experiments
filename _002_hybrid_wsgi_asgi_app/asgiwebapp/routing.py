from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/message/", consumers.MessageConsumer.as_asgi()),
    path(r"ws/heartbeat/", consumers.HeartbeatConsumer.as_asgi()),
]