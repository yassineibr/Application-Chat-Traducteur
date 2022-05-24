import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import PrivateMessages, UserProfile

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chatroom_message',
                'message': message,
                'username': username,
            }
        )
        
    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data = json.dumps({
            'message' : message,
            'username': username,
        }))


class PrivateChatRoomConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_userProfile_id_fr_userId(self, userId ):
        return UserProfile.objects.get(user__pk = userId).id

    @database_sync_to_async
    def getPrivateMessages(self, room_name ):
        return list(PrivateMessages.objects.filter(chatroomname = room_name ))
    
    @database_sync_to_async
    def get_messages_text(self, msg ):
        return msg.text

    @database_sync_to_async
    def get_messages_username(self, msg ):
        return msg.sender.user.username

    @database_sync_to_async
    def setNewPrivateMessages(self, text ):
        PrivateMessages.objects.create(
            chatroomname = self.room_group_name,
            sender=UserProfile.objects.get(pk=self.user_id),
            receiver=UserProfile.objects.get(pk=self.dest_id),
            text=text
        ).save()

    async def connect(self):
        self.user = self.scope['user']
        self.user_id = await self.get_userProfile_id_fr_userId(self.user.id)
        self.dest_id = self.scope['url_route']['kwargs']['dest_id']
        if  self.user_id > int(self.dest_id):
            self.room_group_name = f"prvchat_{self.user_id}_{self.dest_id}"
        else:
            self.room_group_name = f"prvchat_{self.dest_id}_{self.user_id}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()


        for msg in await self.getPrivateMessages(self.room_group_name) :
            message = msg.text
            username = await self.get_messages_username(msg)
            await self.send(text_data = json.dumps({
                'message' : message,
                'username': username,
            }))
            

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.setNewPrivateMessages(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chatroom_message',
                'message': message,
                'username': self.user.username,
            }
        )
        
    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data = json.dumps({
            'message' : message,
            'username': username,
        }))


