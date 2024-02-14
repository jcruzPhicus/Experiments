import json
import random
import time

from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth.models import Permission
import asyncio
from asgiref.sync import sync_to_async, async_to_sync


def get_user_permissions(user):
    if user.is_superuser:
        return list(Permission.objects.all())
    return list(user.user_permissions.all()) | list(Permission.objects.filter(group__user=user))


class BaseJsonConsumer(JsonWebsocketConsumer):

    def __init__(self, group_name: str, valid_message_types, auth_required: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = group_name
        self.valid_message_types = [
            "subscribe", "unsubscribe", "help", *valid_message_types]
        self.auth_required = auth_required

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive_json(self, content):
        try:
            print(content)
            message_type: str = content["type"].lower()
            data = content.get("data")
            message_group_name = data.get(
                "group_name") if data is not None else None
            is_help_message: bool = (
                message_type == "_help" or message_type == "help")
            if message_type not in self.valid_message_types or is_help_message:
                self.send_json({"content": "Wrong message_type"})
            else:
                print(f"Sending to {self.channel_name}, {message_type} {data}")
                async_to_sync(self.channel_layer.send)(
                    self.channel_name, {"type": f"{message_type}", "data": data})
        except KeyError as e:  # Falta un parámetro obligatorio
            self.send_json(content={
                           "message": "You forgot to specify a required parameter.", "exception": str(e)})
        except json.decoder.JSONDecodeError as e:  # No es JSON válido
            self.send_json(
                content={"message": "JSON data is invalid.", "exception": str(e)})


class EchoConsumer(BaseJsonConsumer):
    group_name = "echo"
    valid_message_types = ["message"]

    def __init__(self, *args, **kwargs):
        super().__init__(group_name=self.group_name,
                         valid_message_types=self.valid_message_types, auth_required=False, *args, **kwargs)

    def message(self, event):
        data = event.get("data")
        message = data.get("message") if data else None
        print("Called alert_message")
        time.sleep(2)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "publish", "group_name": self.group_name, "content": message})


class HeartbeatConsumer(WebsocketConsumer):
    groups = ["heartbeat"]

    def publish(self, event):
        pass

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def message(self, event):
        msg = event["message"]
        self.send(text_data=json.dumps({"message": f"{msg}"}))


class AuthConsumer(WebsocketConsumer):
    user = None

    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
        else:

            self.accept()
            self.group_name = self.user.username
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)

    def receive(self, text_data):
        msg = json.loads(text_data)
        msg_type = msg["type"]
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": msg_type})

    def permission(self, event):
        permissions = get_user_permissions(self.user)
        permission_list = []
        for p in permissions:
            permission_list.append(p.name)
        self.send(text_data=json.dumps({"message": permission_list}))

    def username(self, event):
        self.send(text_data=json.dumps({"message": self.user.username}))


class SubscriptionConsumer(BaseJsonConsumer):
    valid_message_types = ["subscribe",
                           "unsubscribe", "publish", "query"]

    group_name = "pubsub"
    subscriptions = {}

    def __init__(self, *args, **kwargs):
        super().__init__(group_name=self.group_name,
                         valid_message_types=self.valid_message_types, auth_required=False, *args, **kwargs)

    def disconnect(self, close_code):
        my_groups = self.subscriptions.setdefault(self.channel_name, [])
        for group in my_groups:
            async_to_sync(self.channel_layer.group_discard)(
                group, self.channel_name)

        self.subscriptions.pop(self.channel_name, [])
        super().disconnect(close_code)

    def subscribe(self, event):
        data = event.get("data")
        group_name = data.get("group_name") if data else None
        my_groups = self.subscriptions.setdefault(self.channel_name, [])
        if not my_groups or group_name not in my_groups:
            async_to_sync(self.channel_layer.group_add)(
                group_name, self.channel_name)
            my_groups.append(group_name)

    def unsubscribe(self, event):
        data = event.get("data")
        group_name = data.get("group_name") if data else None
        my_groups = self.subscriptions.setdefault(self.channel_name, [])
        if my_groups and group_name in group_name:
            async_to_sync(self.channel_layer.group_discard)(
                group_name, self.channel_name)
            my_groups.remove(group_name)

    def query(self, event):
        my_groups = self.subscriptions.setdefault(self.channel_name, [])
        self.send_json({"groups": my_groups})

    def publish(self, event):
        print(event)
        print(self.channel_name)
        content = event.get("content")
        group_name = event.get("group_name")
        self.send_json({"group_name": group_name, "content": content})
