from channelsmultiplexer import AsyncJsonWebsocketDemultiplexer
from channels_demultiplexer.demultiplexer import WebsocketDemultiplexer
from .consumers import EchoConsumer, HeartbeatConsumer, SubscriptionConsumer


class Demultiplexer(AsyncJsonWebsocketDemultiplexer):
    # Wire your async JSON consumers here: {stream_name: consumer}
    applications = {
        "echo": EchoConsumer.as_asgi(),
        "heartbeat": HeartbeatConsumer.as_asgi(),
        "pubsub": SubscriptionConsumer.as_asgi()
    }


""" class Demultiplexer(WebsocketDemultiplexer):
    # Wire your async JSON consumers here: {stream_name: consumer}
    consumer_classes = {
        "echo": EchoConsumer,
        "heartbeat": HeartbeatConsumer,
        "pubsub": SubscriptionConsumer
    }
 """
