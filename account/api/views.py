from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework import generics, permissions, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


from account.models import *
from account.api.serializers import *


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from hashlib import sha256

# @swagger_auto_schema(method='put', auto_schema=None)
# @swagger_auto_schema(methods=['get'], ...)
# @api_view(['GET', 'PUT'])

# test_param = openapi.Parameter('test', openapi.IN_QUERY,description="test manual param", type=openapi.IN_BODY)
user_response = openapi.Response('response description', UserSignupSerializer)
user_response1 = openapi.Response('response description', RequestLoginSerializer)
user_response2 = openapi.Response('bad request')

# @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})


class SignupView(APIView):
    # @swagger_auto_schema(operation_description="partial_update description override", responses={404: 'slug not found'})
    # @swagger_auto_schema(method='post', manual_parameters=[test_param], responses={200: user_response})
    # @api_view(['POST'])
    @swagger_auto_schema(
    operation_description="apiview post description override",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['password','username','gender','email','nickname'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': { "type": "string", "format": "password"},
                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                'email': { "type": "string", "format": "email"},
                'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                'birthdate': { "type": "string", "format": "date"}
            },
        ),
        security=[],
        tags=['Users']
        ,responses={200: user_response,400:user_response2}
     )
    # @swagger_auto_schema(request_body=UserSignupSerializer, tags=['Users'],responses={200: user_response,400:user_response2})
    @csrf_exempt
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            u = serializer.save()
            login(request, u)
            info = UserInfoSerializer(u)
            print(u)
            return Response({
                'message': 'your account have been created successfuly',
                'data': info.data
            })
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    @swagger_auto_schema(request_body=RequestLoginSerializer, tags=['Users'],responses={200: user_response1,400:user_response2})
    @csrf_exempt
    def post(self, request):
        print("fdsbioiobuiio")
        serializer = RequestLoginSerializer(data=request.data)
        if serializer.is_valid():
            u = authenticate(
                request,
                username=serializer.data['username'],
                password=serializer.data['password'])
            if u is None:
                return Response(
                    {
                        'message': 'The username or password is wrong'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            if u:
                #successful request
                login(request, u)
                user = CustomUser.object.get(id = u.id)
                user.status = "online"
                print(user.status)
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
                        'message': 'The username or password is wrong'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
# user profile
