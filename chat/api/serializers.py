from rest_framework import serializers
from account.models import CustomUser as User
from ..models import Message, Conversation
from TunePal import settings
from datetime import datetime
from django.db.models import Q




class UserProfileSerilizer(serializers.ModelSerializer):
    to_show = serializers.SerializerMethodField()

    def get_to_show(self, obj):
        return not obj == self.context['request'].user

    class Meta(object):
        model = User
        fields = ['id','username', 'nickname','status','to_show','user_avatar']
        extra_kwargs ={'to_show':{'required': False}}


class ConversationSerializer(serializers.ModelSerializer):
    new_messages = serializers.SerializerMethodField()
    members = UserProfileSerilizer(many = True)
    last_message = serializers.SerializerMethodField()

    def get_last_message(self, obj):
        user = self.context['request'].user
        last_message = Messages.objects.filter(Q(conversation_id = obj))[-1]
        serilizer = MessageSerializer(last_message)
        return serilizer

    def get_new_messages(self, obj):
        user = self.context['request'].user
        new_recieved_messages = len(Messages.objects.filter(Q(conversation_id = obj)).filter(~Q(sender_id=u)).filter(Q(is_seen=False)))
        return new_recieved_messages

    class Meta(object):
        model = Conversation
        fields = ['members','id','is_group']
        extra_kwargs = {'is_group':  {'required': False}}
        
    
class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserProfileSerilizer(required=False)
    is_client = serializers.SerializerMethodField()

    def get_is_client(self, obj):
        return obj.sender_id == self.context['request'].user

    class Meta(object):
        model = Message
        fields = ["sender_id" ,"conversation_id", "text" ,"date" , "is_client"]
        extra_kwargs = {'is_client':  {'required': False},
                        'date':  {'required': False},
                        'sender_id':  {'required': False},
                        'conversation_id':  {'required': False}
                        }

    def create(self, validated_data, *args, **kwargs):
        user =  self.context['request'].user
        conversation = self.context['coversation_id']
        u = Message(sender_id = user,
                conversation_id = conversation,
                text = validated_data['text'],
                date = datetime.now()
                )
        u.save()
        return u

     
    #def create(self, validated_data):
    #     user =  self.context['request'].user
    #     u = Conversation(name = user,
    #             members =c
    #             )
    #     u.save()
    #     return u
 
