from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/message/", consumers.MessageConsumer.as_asgi()),
]