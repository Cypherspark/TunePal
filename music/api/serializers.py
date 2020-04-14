from rest_framework import serializers
from account.models import CustomUser as User
from account.models import Friend
from TunePal import settings


# class FriendInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Friend
#         fields = ["username","nickname"]
