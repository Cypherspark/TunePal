rom django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, permissions, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from account.models import User
from . import serializers




class UserRegistrationAPIView(generics.CreateAPIView):
    """
    Endpoint for user registration.
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserRegistrationSerializer
    queryset = User.objects.all()
