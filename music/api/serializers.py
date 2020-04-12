from rest_framework import serializers
from account.models import CustomUser as User
from account.models import Friends
from music.models import User_top_music,Quiz
from TunePal import settings


class FriendInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ["username","nickname"]
# class UserScoreAndArtist(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['top_artist','score']
# show top song
class UserTopSongserialize(serializers.ModelSerializer):
    class Meta:
        model = User_top_music
        fields = ['artist_name','music_name','album']
class UserProfileUpdateScore(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['score']
class Userprivatequiz(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["question",'choices1','choices2','choices3','choices4']
class Checkserialiser(serializers.ModelSerializer):
            class Meta:
                model = Quiz
                fields = ["quiz_id",'answer']
