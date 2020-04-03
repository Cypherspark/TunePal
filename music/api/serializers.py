from rest_framework import serializers
from account.models import CustomUser as User
from account.models import Friends
from TunePal import settings


class FriendInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ["username","nickname"]
