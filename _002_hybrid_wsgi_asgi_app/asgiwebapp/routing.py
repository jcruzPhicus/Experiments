from django.urls import path

from . import consumers
from . import demultiplexer
websocket_urlpatterns = [
    path(r"ws/", demultiplexer.Demultiplexer.as_asgi())
]
