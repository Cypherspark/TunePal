from rest_framework import serializers
from music.models import User_top_music
from account.models import CustomUser as User
from account.models import Friend, Suggest, UserLocation, FriendshipRequest
from TunePal import settings
from random import seed
from random import randint
from datetime import date

seed(1)




class LocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserLocation
        fields = '__all__'

class UserTopSongserialize(serializers.ModelSerializer):
    class Meta:
        model = User_top_music
        fields = ['artist_name','music_name','album']


class UserInfoSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        today = date.today()
        birthDate = obj.birthdate
        try:
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        except:
            age = 20
        return age 
        

    def get_location(self, obj):
        return hash(obj.username)%100
	
    class Meta:
        model = User
        fields = ["gender","location","nickname","username","user_avatar","age"]


class UserInfoSerializer1(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    pendding = serializers.SerializerMethodField()

    def get_pendding(self, obj):
        try:
            relation = FriendshipRequest.objects.get(to_user=obj, from_user=self.context['request'].user)  
            status = relation.accepted
        except:
            status = False

        return status


    def get_age(self, obj):
        today = date.today()
        birthDate = obj.birthdate
        try:
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        except:
            age = 20
        return age 
        

    def get_location(self, obj):
        return hash(obj.username)%100
	
    class Meta:
        model = User
        fields = ["gender","location","nickname","username","user_avatar","age",'pendding']


class SuggestInfoSerializer(serializers.ModelSerializer):
    s_users = UserInfoSerializer1(many = True)

    class Meta:
        model = Suggest
        fields = "__all__"


class FriendshipInfoSerializer(serializers.ModelSerializer):
    to_user = UserInfoSerializer()

    class Meta:
        model = FriendshipRequest
        fields = ['to_user']

# location
# username
# gender
# nickname
# user_avatar
# age - birthdate