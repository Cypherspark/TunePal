
from rest_framework import generics, permissions, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from account.api.serializers import *

class SignupView(APIView):

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            u = serializer.save()
            print(u)
            return Response({
                'message': 'your account have been created successfuly',
                'data': serializer.data
            })
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )






# class UserRegistrationAPIView(generics.CreateAPIView):
#     """
#     Endpoint for user registration.
#     """
#     permission_classes = (permissions.AllowAny, )
#     serializer_class = serializers.UserRegistrationSerializer
#     queryset = User.objects.all()
# ``