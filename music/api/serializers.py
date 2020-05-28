from rest_framework import serializers
from music.models import Music
from account.models import CustomUser as User
from account.models import Friend, Suggest, UserLocation, FriendshipRequest, Avatar
from TunePal import settings
from random import seed
from random import randint
from datetime import date

from math import sin, cos, sqrt, atan2, radians


seed()

class UserAvatarSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["image","id"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserLocation
        fields = '__all__'

class UserTopSongserialize(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['track_name','artist_name','album','image_url','spotify_url']


class UserInfoSerializer2(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    user_avatar = UserAvatarSerializer1(many = True)

    def get_age(self, obj):
        today = date.today()
        birthDate = obj.birthdate
        try:
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        except:
            age = 20
        return age


    def get_location(self, obj):
        try:
            dlon = self.context['request'].user.location.longitude - obj.location.longitude
            dlat = self.context['request'].user.location.latitude - obj.location.latitude
            R = 6373.0


            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
        except:
            distance = None

        return distinct
            
    class Meta:
        model = User
        fields = ["gender","location","nickname","username","user_avatar","age"]


class UserInfoSerializer1(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    pendding = serializers.SerializerMethodField()
    user_avatar = UserAvatarSerializer1(many = True)

    def get_pendding(self, obj):
        try:
            relation = FriendshipRequest.objects.get(to_user=obj, from_user=self.context['request'].user)
            status = True
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
        try:
            dlon = self.context['request'].user.location.longitude - obj.location.longitude
            dlat = self.context['request'].user.location.latitude - obj.location.latitude
            R = 6373.0

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
        except:
            distance = None
        return distance

    class Meta:
        model = User
        fields = ["gender","location","nickname","username","user_avatar","age",'pendding']


class SuggestInfoSerializer(serializers.ModelSerializer):
    s_users = UserInfoSerializer1(many = True)

    class Meta:
        model = Suggest
        fields = ['s_users']

class FriendshipInfoSerializer(serializers.ModelSerializer):
    from_user = UserInfoSerializer2()

    class Meta:
        model = FriendshipRequest
        fields = ['from_user']

# location
# username
# gender
# nickname
# user_avatar
# age - birthdate
