import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import GroupChatRoom, GroupMessage

class CohortChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("[DEBUG] WebSocket connect() called")

        self.cohort_year = self.scope['url_route']['kwargs'].get('cohort_year')
        print(f"[DEBUG] cohort_year from URL: {self.cohort_year}")

        self.group_name = f"cohort_chat_{self.cohort_year}"
        print(f"[DEBUG] Group name: {self.group_name}")

        try:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            print("[DEBUG] Connection accepted and added to group")
        except Exception as e:
            print(f"[ERROR] connect() failed: {e}")

    async def disconnect(self, close_code):
        print(f"[DEBUG] Disconnecting. Close code: {close_code}")
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("[DEBUG] Disconnected cleanly")

    async def receive(self, text_data):
        print(f"[DEBUG] Raw data received: {text_data}")
        try:
            data = json.loads(text_data)
            message_text = data.get('text')
            user = self.scope.get('user')

            print(f"[DEBUG] Parsed message: {message_text}")
            print(f"[DEBUG] From user: {user.username if user and user.is_authenticated else 'Anonymous'}")

            # Save to DB
            room, _ = await sync_to_async(GroupChatRoom.objects.get_or_create)(cohort_year=self.cohort_year)
            await sync_to_async(GroupMessage.objects.create)(room=room, sender=user, text=message_text)
            print("[DEBUG] Message saved to DB")

            # Broadcast
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'broadcast_message',
                    'text': message_text,
                    'sender': user.username if user and user.is_authenticated else 'Anonymous'
                }
            )
            print("[DEBUG] Broadcast sent to group")

        except Exception as e:
            print(f"[ERROR] receive() failed: {e}")

    async def broadcast_message(self, event):
        print(f"[DEBUG] Broadcasting message: {event}")
        try:
            await self.send(text_data=json.dumps({
                'text': event['text'],
                'sender': event['sender']
            }))
            print("[DEBUG] Message sent back to WebSocket client")
        except Exception as e:
            print(f"[ERROR] broadcast_message() failed: {e}")
