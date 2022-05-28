import json
from textblob import TextBlob
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import PrivateMessages, TranslatedPrivateMessages, UserProfile

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
    def getPrivateMessages(self, room_name ):
        return list(PrivateMessages.objects.filter(chatroomname = room_name ))
    
    @database_sync_to_async
    def get_text_username_from_msg(self, msg : PrivateMessages) :
        return msg.text, msg.sender.user.username

    @database_sync_to_async
    def get_translated_text_username_from_msg(self, msg : PrivateMessages) :
        transMsg = TranslatedPrivateMessages.objects.get(srcMessage=msg)
        return transMsg.text, msg.sender.user.username

    @database_sync_to_async
    def setNewPrivateMessages(self, text):
        new_msg =  PrivateMessages.objects.create(
            chatroomname = self.room_group_name,
            sender=UserProfile.objects.get(pk=self.user_id),
            receiver=UserProfile.objects.get(pk=self.dest_id),
            text=text
        )
        new_msg.save()
        return new_msg

    @database_sync_to_async
    def setTranslatedMessage(self, prvMsg : PrivateMessages):
        srcText = TextBlob(prvMsg.text)

        src_lang = prvMsg.sender.languageKey
        dest_lang = prvMsg.receiver.languageKey

        try : 
            translatedText = str(srcText.translate(from_lang=src_lang, to = dest_lang)) # TODO
        except:
            return prvMsg

        translatedMsg =  TranslatedPrivateMessages.objects.create(
            srcMessage = prvMsg,
            text = translatedText
        )
        translatedMsg.save()
        return translatedMsg

    @database_sync_to_async
    def toTranslate(self ) -> bool :
        return self.src_user.languageKey != self.dest_user.languageKey

    @database_sync_to_async
    def get_userProfile(self, user_id):
        return UserProfile.objects.get(user__pk=user_id)

    async def connect(self):
        self.user = self.scope['user']
        self.dest_id = self.scope['url_route']['kwargs']['dest_id']
        self.dest_user = await self.get_userProfile(self.dest_id)
        self.src_user = await self.get_userProfile(self.user.id)
        self.user_id = self.src_user.id
        self.translate = await self.toTranslate()

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
            message, username = await self.get_text_username_from_msg(msg)
            if self.toTranslate:
                try :
                    translated_text, username = await self.get_translated_text_username_from_msg(msg)
                    if self.src_user.languageKey == msg.sender.languageKey:
                        await self.send(text_data = json.dumps({
                            'message' : message,
                            'username' : username,
                        }))
                    else : 
                        await self.send(text_data = json.dumps({
                            'message' : translated_text,
                            'username' : username,
                        }))
                except:
                    await self.send(text_data = json.dumps({
                        'message' : message,
                        'username': username,
                    }))

            else : 
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
        new_msg = await self.setNewPrivateMessages(message)
        if self.toTranslate:
            translated_msg = await self.setTranslatedMessage(new_msg)
        else :
            translated_msg = new_msg

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chatroom_message',
                'src_message' : new_msg,
                'translated_message' : translated_msg,
            }
        )
        
    async def chatroom_message(self, event):
        new_msg = event['src_message']
        text, username = await self.get_text_username_from_msg(new_msg) 
        if self.toTranslate:
            trans_msg = event['translated_message']
            translated_text = trans_msg.text
            if self.src_user.languageKey == new_msg.sender.languageKey:
                await self.send(text_data = json.dumps({
                    'message' : text,
                    'username' : username,
                }))
            else : 
                await self.send(text_data = json.dumps({
                    'message' : translated_text,
                    'username' : username,
                }))
        else : 
            await self.send(text_data = json.dumps({
                'message' : text,
                'username': username,
            }))
