import json
import random
import time

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth.models import Permission
import asyncio
from asgiref.sync import sync_to_async, async_to_sync

def get_user_permissions(user):
    if user.is_superuser:
        return list(Permission.objects.all())
    return list(user.user_permissions.all()) | list(Permission.objects.filter(group__user=user))

class MessageConsumer(WebsocketConsumer):
    group_name = "grupoTest"
    user = None


    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.accept() # realmente esto debería de hacerlo el frontend, si falla la conexion enseñar error, en vez de aceptar y cerrar
            self.send(text_data=json.dumps({"message": f"You are not logged in, go to /login and try again."}))
            self.close()
        else: 
            permissions = get_user_permissions(self.user)
            self.accept()
            self.group_name = self.user.username
            self.send(text_data=json.dumps({"message": f"You are logged in as {self.user} with permissions {permissions}"}))
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)
        async_to_sync(self.channel_layer.group_send)(self.group_name, {"type": "alert.message", "message": message})
    
    def alert_message(self, event):
        message = event["message"]
        print("Called alert_message")
        time.sleep(2)
        self.send(text_data=json.dumps({"message": f"You sent {message}!"}))


class HeartbeatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept() 
        await asyncio.get_event_loop().create_task(self.send_heartbeat())
            

    async def disconnect(self, close_code):
        await self.close()
    
    async def send_heartbeat(self):
        await asyncio.sleep(5)
        await self.send(text_data=json.dumps({"message": f"Heartbeat at {time.strftime('%m/%d/%Y, %H:%M:%S', time.localtime())}"}))
        await asyncio.get_event_loop().create_task(self.send_heartbeat())


class AuthConsumer(WebsocketConsumer):
    user = None
    
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
        else: 
            
            self.accept()
            self.group_name = self.user.username
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        msg = json.loads(text_data)
        msg_type = msg["type"]
        async_to_sync(self.channel_layer.group_send)(self.group_name, {"type": msg_type})



    def permission(self, event):
        permissions = get_user_permissions(self.user)
        permission_list = []
        for p in permissions:
            permission_list.append(p.name)
        self.send(text_data=json.dumps({"message": permission_list}))

    def username(self, event):
        self.send(text_data=json.dumps({"message": self.user.username}))