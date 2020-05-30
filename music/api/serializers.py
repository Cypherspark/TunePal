from rest_framework import serializers
from music.models import Music
from account.models import CustomUser as User
from account.models import Friend, Suggest, UserLocation, FriendshipRequest, Avatar
from TunePal import settings
from random import seed
from random import randint
from datetime import date
import json
from django.http import JsonResponse
import math
import geopy.distance

from math import sin, cos, sqrt, atan2, radians


seed()

class UserAvatarSerializer1(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

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
    user_avatar = serializers.SerializerMethodField()

    def get_user_avatar(self, obj ):
        user = obj
        serializer = UserAvatarSerializer1(user.user_avatar,many = True)
        try:
            avatar = serializer.data[-1]
        except:
            avatar = None
        return avatar

    def get_age(self, obj):
        today = date.today()
        birthDate = obj.birthdate
        try:
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        except:
            age = 20
        return age


    def get_location(self, obj):
        if hasattr(obj.location, 'longitude') and hasattr(self.context['request'].user.location, 'longitude')  :
            coords_1 = (self.context['request'].user.location.latitude, self.context['request'].user.location.longitude)
            coords_2 = (obj.location.latitude, obj.location.longitude)
            distance = round(geopy.distance.vincenty(coords_1, coords_2).km)
        else:
            distance = None
        return distance


    class Meta:
        model = User
        fields = ["gender","location","nickname","username","user_avatar","age"]




class UserInfoSerializer1(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    pendding = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()

    def get_user_avatar(self, obj ):
        user = self.context['request'].user
        serializer = UserAvatarSerializer1(user.user_avatar,many = True)
        try:
            avatar = serializer.data[-1]
        except:
            avatar = None
        return avatar

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


    def get_location(self, obj) :
        if hasattr(obj.location, 'longitude') and hasattr(self.context['request'].user.location, 'longitude')  :
            coords_1 = (self.context['request'].user.location.latitude, self.context['request'].user.location.longitude)
            coords_2 = (obj.location.latitude, obj.location.longitude)
            distance = round(geopy.distance.vincenty(coords_1, coords_2).km)
        else:
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
