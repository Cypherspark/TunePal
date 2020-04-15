from rest_framework import serializers
from account.models import CustomUser as User
from ..models import Message, Conversation
from TunePal import settings
from datetime import datetime


class MessageSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Message
        fields = "__all__"
        extra_kwargs = {'is_seen':  {'required': False}}

    def create(self, validated_data):

        user =  self.context['request'].user
        u = Message(sender_id = user,
                conversation_id = c,
                text = validated_data['text'],
                date = datetime.now()
                )
        u.save()
        return u

class ConversationSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Conversation
        fields = "__all__"
        extra_kwargs = {'is_group':  {'required': False}}


class UserProfileSerilizer(serializers.ModelSerializer):

    class Meta(object):
        model = Conversation
        fields = ['username','gender', 'nickname'}
        
    
    
    
    
    
    #def create(self, validated_data):
    #     user =  self.context['request'].user
    #     u = Conversation(name = user,
    #             members =c,
    #             text =validated_data['text'],
    #             )
    #     u.save()
    #     return u
 
