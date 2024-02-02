import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
import asyncio
from asgiref.sync import async_to_sync
class MessageConsumer(AsyncWebsocketConsumer):
    group_name = "grupoTest"
    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)
        await self.channel_layer.group_send(self.group_name, {"type": "alert.message", "message": message})
    
    async def alert_message(self, event):
        message = event["message"]
        print("Called alert_message")
        await asyncio.sleep(2)
        await self.send(text_data=json.dumps({"message": f"You sent {message}!"}))
       