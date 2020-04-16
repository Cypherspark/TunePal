from rest_framework import serializers
from music.models import User_top_music
from account.models import CustomUser as User
from account.models import Friend
from TunePal import settings


class UserTopSongserialize(serializers.ModelSerializer):
    class Meta:
        model = User_top_music
        fields = ['artist_name','music_name','album']


# class FriendInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Friend
#         fields = ["username","nickname"]
