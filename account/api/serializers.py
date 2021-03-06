from datetime import date
from rest_framework import serializers
from account.models import CustomUser as User,Avatar
from account.models import UserLocation
from TunePal import settings




def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


class SetUserAvatarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Avatar
        fields = ["image"]


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["image","id"]


class UserSignupSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        label="Email Address"
    )

    password = serializers.CharField(
        required=True,
        label="Password",
        style={'input_type': 'password'}
    )

    username = serializers.CharField(
        label="Username",
        required=True
    )

    birthdate = serializers.DateField(
        label="Birthdate",
        required=True
    )
    gender = serializers.CharField(
        label="Gender",
        required=True
    )
    nickname = serializers.CharField(
        label="Name",
        required=True
    )

    class Meta(object):
        model = User
        fields = ['username', 'email', 'password', 'birthdate', 'gender', 'nickname','biography','interests']
        extra_kwargs = {'biography':  {'allow_null': True, 'required': False},
        'interests': {'allow_null': True, 'required': False},

        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def validate_birthdate(self, value):
        if calculateAge(value) < 18 :
            raise serializers.ValidationError("You must be over 18 to continue.")
        return value

    def create(self, validated_data):

        user_data = User(
            nickname = validated_data.get('nickname'),
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            birthdate= validated_data.get('birthdate'),
            gender = validated_data.get('gender'),
        )
        user_data.set_password(validated_data['password'])
        user_data.save()
        return user_data

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance




class RequestLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=30, allow_blank=False,
    )
    password = serializers.CharField(
        required=True, max_length=128, allow_blank=False
    )


class LocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserLocation
        fields = '__all__'
        extra_kwargs = {'latitude':  {'write_only': True},'longitude':  {'write_only': True}}
    def create(self, validated_data):
        ulocation = UserLocation(
            latitude = validated_data.get("latitude"),
            longitude = validated_data.get("longitude"),
            country = validated_data.get("country"),
            province = validated_data.get("province"),
            neighbourhood = validated_data.get("neighbourhood")
        )
        ulocation.save()
        return ulocation

class UserInfoSerializer(serializers.ModelSerializer):
    user_avatar = UserAvatarSerializer(many = True)
    # serializers.SerializerMethodField()
    # interest = UserInterestsSerializer(read_only =True)
    location = LocationSerializer(read_only =True)

    # def get_user_avatar(self, user):
    #     photo_url = user.user_avatar
    #     return request.build_absolute_uri(photo_url)

    class Meta:
        model = User
        fields = ['username', 'email', 'birthdate', 'gender', 'nickname','biography','interests','score','location','user_avatar']






# class UserInterestsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fiels = ['interests']
