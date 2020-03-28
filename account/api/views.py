rom django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, permissions, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from account.models import User
from . import serializers


class LoginView(APIView):
    
    @swagger_auto_schema(request_body=RequestLoginSerializer, tags=['Users'],responses={200: user_response1,400:user_response2})
    def post(self, request):
        serializer = RequestLoginSerializer(data=request.data)
        if serializer.is_valid():
            u = authenticate(
                request,
                username=serializer.data['username'],
                password=serializer.data['password'])
            if u is None:
                return Response(
                    {
                        #wrong_username
                        'message': 'There is not any account with this username'
                    },
                    status=status.HTTP_404_NOT_FOUND
                ) 
            if u:#successful request
                print(u)
                print('here')
                login(request, u)
                return Response(
                    {
                        'message': 'Your account info is correct',
                        'data': {
                            'username': u.username,
                            "id": u.id,
                        }
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        #wrong_pass
                        'message': 'Your password is wrong'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    Endpoint for user registration.
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserRegistrationSerializer
    queryset = User.objects.all()
