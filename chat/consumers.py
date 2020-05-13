import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Conversation,Message
from account.models import CustomUser as User
from chat.api.serializers import MessageSerializer
from rest_framework import serializers

from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    # def __init__(self):
    user_room_name= 'football'
    sender_id = User
    # conversation_id = Conversation.obects.all()[0]
    # userparameter = 0
    def connect(self):
        
        self.user = self.scope["user"]
        print(self.user,scope["header"])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        message = text_data_json['message']
        # print(self.length)
        # Send message to room group

        if self.room_name ==self.user_room_name:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
            # GroupMessage.objects.create(sender_id =self.sender_id,conversation_id =self.conversation_id,text = message)
            c = Conversation.objects.get(id = self.room_name)
            messege = Message.objects.create(sender_id =self.user,conversation_id = c ,text = messege,date = datetime.now() )

  

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # GroupMessage.objects.create(sender_id,conversation_id,message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
    # def a(self):
    #     print("sedhsioahoiguk")
