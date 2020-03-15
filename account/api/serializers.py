from datetime import date 
from rest_framework import serializers
from account.models import User
from TunePal import settings

  
def calculateAge(birthDate): 
    today = date.today() 
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    return age 

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

    # password_2 = serializers.CharField(
    #     required=True,
    #     label="Confirm Password",
    #     style={'input_type': 'password'}
    # ) 

    first_name = serializers.CharField(
        required=True
    )

    last_name = serializers.CharField(
        required=True
    )

    birthdate = serializers.DateField(
        required=True
    )

    class Meta(object):
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'birthdate', 'gender']

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

    # def validate_password_2(self, value):
    #     data = self.get_initial()
    #     password = data.get('password')
    #     if password != value:
    #         raise serializers.ValidationError("Passwords doesn't match.")
    #     return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_birthdate(self, value):
        if calculateAge(value) < 18 :
            raise serializers.ValidationError("You must be over 18 to continue.")
        return value
        
    def create(self, validated_data):

        password1 = User.hash_password(validated_data.get('password')),
         
        user_data = User(
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            first_name= validated_data.get('first_name'),
            last_name= validated_data.get('last_name'),
            birthdate= validated_data.get('birthdate'),
            gender = validated_data.get('gender'),
            password = password1
        )
        password = validated_data.get('password'),
        user_data.save()
        return user_data
