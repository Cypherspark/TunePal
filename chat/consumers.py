import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Conversation,Message
from account.models import CustomUser as User
from chat.api.serializers import MessageSerializer
from rest_framework import serializers
from channels.db import database_sync_to_async
from datetime import datetime
 

@database_sync_to_async
def make_seen(message_ID):
    messageObject = Message.objects.get(id = message_ID)
    messageObject.is_seen = True
    messageObject.save()

@database_sync_to_async
def get_user(userName):
    return User.objects.get(username = userName)

@database_sync_to_async
def make_message(user ,message , ID):
    c = Conversation.objects.get(id = ID)
    messageObject = Message.objects.create(sender_id = user,conversation_id = c ,text = message,date = datetime.now() )
    return messageObject.id

@database_sync_to_async
def GroupInfo(ID):
    c = Conversation.objects.get(id = ID)
    flag = c.is_group
    name = c.name
    return [flag, name]


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        # self.user = self.scope["user"]
        # print("-------> i'm ",self.user)
        # print(self.scope["headers"])
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        user_id = self.scope['url_route']['kwargs']['room_name']
        self.user = await get_user(user_id)
        # print("----ddddddd---> i'm ", user_id)
        user_id = self.user.id 
        print("-------> i'm ", self.user)
        # self.room_group_name = 'chat_%s' % self.room_name
        self.room_group_name =  "{}".format(user_id)
        # Join room groupis_group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['text']
        ID = text_data_json['id']

        messageID = await make_message(self.user , message, ID)
        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         "messageID" : messageID,
        #         "date" : f"",
        #         'type': 'chat_message',
        #         'message': message,
        #         'username': self.user.username,
        #         'nickame': self.user.nickname,
        #         'conversation_id': ID
                
        #     }
        # )
        

  

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        date1 = event['date']
        date = date1.replace(" ", "T") + "Z"
        username = event['username']
        nickname = event['nickame']
        conversation_id = event['conversation_id']

        is_me = (username == self.user.username)
        if not is_me:
            await make_seen(int(event['messageID']))
        info = await GroupInfo(int(conversation_id))
        is_group = info[0]
        name = info[1]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "group_name" : name,
            "is_group": is_group,
            "date" : date,
            'is_client': is_me,
            "sender_id" : {"nickname":nickname} ,
            "text": message,
            "conversation_id":conversation_id           
        }))    