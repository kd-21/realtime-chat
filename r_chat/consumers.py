# r_chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from r_chat.models import Room, Messages, User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f"chat_{self.room_slug}"

        try:
            self.room = await sync_to_async(Room.objects.get)(slug=self.room_slug)
        except Room.DoesNotExist:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"WebSocket connected to {self.room_group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected from {self.room_group_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        username = data.get("username")

        if message and username:
            await self.save_message(message, username)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_message",
                    "message": message,
                    "username": username,
                }
            )

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"]
        }))

    async def save_message(self, message, username):
        try:
            user = await sync_to_async(User.objects.get)(username=username)
            await sync_to_async(Messages.objects.create)(
                room=self.room,
                user=user,
                content=message
            )
            print(f"Message saved: {message}")
        except User.DoesNotExist:
            print(f"User '{username}' does not exist.")
