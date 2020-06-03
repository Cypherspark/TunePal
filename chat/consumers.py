import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Conversation,Message
from account.models import CustomUser as User
from chat.api.serializers import MessageSerializer
from rest_framework import serializers
from channels.db import database_sync_to_async
from datetime import datetime
 

@database_sync_to_async
def make_seen(message_ID):
    messageObject = Message.objects.get(message_ID)
    messageObject.is_seen = True
    messageObject.save()

@database_sync_to_async
def get_user(userName):
    return User.objects.get(username = userName).username

@database_sync_to_async
def get_user_id(userName):
    return User.objects.get(username = userName).id


class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        
        # self.user = self.scope["user"]
        # print("-------> i'm ",self.user)
        # print(self.scope["headers"])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user_id = self.scope['url_route']['kwargs']['room_name']
        self.user = get_user(user_id)
        # user_id = get_user_id(user_id) 
        print("-------> i'm ", self.user)
        print("?????????????", user_id)
        # self.room_group_name = 'chat_%s' % self.room_name
        self.room_group_name =  "{}".format(user_id)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )


        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['text']
        c = Conversation.objects.get(id = self.room_name)
        messageObject = Message.objects.create(sender_id =self.user,conversation_id = c ,text = message,date = datetime.now() )
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "messageID" : messageObject.id,
                "date" : f"{datetime.now()}",
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'nickame': self.user.nickname
                
            }
        )
        

  

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        date1 = event['date']
        date = date1.replace(" ", "T") + "Z"
        username = event['username']
        nickname = event['nickame']
        is_me = (username == self.user.username)
        if not is_me:
            make_seen(int(event['messageID']))
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "conversation_id": self.room_name,
            "date" : date,
            'is_client': is_me,
            "sender_id" : {"nickname":nickname} ,
            "text": message,            
        }))    