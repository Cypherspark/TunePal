from rest_framework import serializers
from account.models import CustomUser as User,Avatar
from ..models import Message, Conversation
from TunePal import settings
from datetime import datetime
from django.db.models import Q




class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["image","id"]


class UserProfileSerilizer(serializers.ModelSerializer):
    to_show = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()

    def get_user_avatar(self, obj ):
        user = self.context['request'].user
        serializer = UserAvatarSerializer(user.user_avatar,many = True)
        return Response(serializer.data[-1])

    def get_to_show(self, obj):
        return not obj == self.context['request'].user

    class Meta(object):
        model = User
        fields = ['id','username', 'nickname','status','to_show','user_avatar']
        extra_kwargs ={'to_show':{'required': False}}


class ConversationSerializer(serializers.ModelSerializer):
    members = UserProfileSerilizer(many = True,required=False)
    new_messages = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_last_message(self, obj):
        request = self.context['request']
        user = request.user
        try:
            last_messageop = Message.objects.filter(Q(conversation_id = obj))[0]
            serilizer = MessageSerializer(last_messageop,context={'request': request})
            data = {"nickname" :serilizer.data['sender_id']['nickname'],
                    "text": serilizer.data["text"]
                    }
        except Exception as e:
            print(str(e))
            serilizer = {}
            data = serilizer
        return data

    def get_new_messages(self, obj):
        user = self.context['request'].user
        new_recieved_messages = len(Message.objects.filter(Q(conversation_id = obj)).filter(~Q(sender_id=user)).filter(Q(is_seen=False)))
        return new_recieved_messages

    class Meta(object):
        model = Conversation
        fields = ['members','id','is_group','new_messages','last_message']
        extra_kwargs = {'is_group':  {'required': False},'new_messages':  {'required': False},'last_message':{'required': False}}




class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserProfileSerilizer(required=False)
    is_client = serializers.SerializerMethodField()

    def get_is_client(self, obj):
        return obj.sender_id == self.context['request'].user

    class Meta(object):
        model = Message
        fields = ["sender_id" ,"conversation_id", "text" ,"date" , "is_client",'is_seen']
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
