from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

import os
import json
import sys
from account.models import CustomUser, Suggest, Friend, FriendshipRequest
from chat.models import Conversation
import spotipy
from spotipy import oauth2
import spotipy.util as util
from music.views import *
from music.api.serializers import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


import random

SPOTIPY_CLIENT_ID = 'c42e107d3ae641e4af9e08e7d7a55b9b'
SPOTIPY_CLIENT_SECRET = 'cd1e4e0aa3684e34ae12b313ebea1074'
SPOTIPY_REDIRECT_URI = 'http://localhost:3000/spotifyresult/'
SCOPE = 'user-top-read user-read-currently-playing user-read-playback-state user-library-read'
CACHE = '.spotipyoauthcache'



sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return Response(
        {"spotifyurl":auth_url},
        status=status.HTTP_200_OK
       )



class SpotifyView(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        return getSPOauthURI()


class SpotifyGetTokenView(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        access_token = ""

        token_info = sp_oauth.get_cached_token(request)
        if token_info:
            print ("Found cached token!fildshcilk")
            access_token = token_info['access_token']
        else:
            url = request.build_absolute_uri()
            code = sp_oauth.parse_response_code(url)
            if code:
                print ("Found Spotify auth code in Request URL! Trying to get valid access token...")
                token_info = sp_oauth.get_access_token(code,request=request)
                access_token = token_info['access_token']

        if access_token:
            print ("Access token available! Trying to get user information...")
            sp = spotipy.Spotify(access_token)
            results = sp.current_user()
            return Response({"url":"http://localhost:3000/spotifyresult/"})


class SuggestUserView(APIView):
    @swagger_auto_schema(tags=['Match'],responses={200: openapi.Response('ok', SuggestInfoSerializer)})
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        user = request.user
        try:
            suggetionlist = Suggest.objects.get(s_current_user = request.user)
        except:
            random.seed()
            slist = random.sample(list(User.objects.exclude(id = request.user.id)),4)
            suggetionlist = Suggest(s_current_user = request.user)
            suggetionlist.save()
            suggetionlist.s_users.add(*slist)


        serializer = SuggestInfoSerializer(suggetionlist, context={'request':request})



        return Response(
                serializer.data,
                status=status.HTTP_200_OK)



class Friend_Request(APIView):
    @swagger_auto_schema(tags=['Match'],responses={200: openapi.Response('ok')})
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        username  = request.GET['username']
        n_f = get_object_or_404(User, username=username)
        owner = request.user
        FR = FriendshipRequest(from_user=owner, to_user=n_f)
        FR.save()
        return Response(status=status.HTTP_200_OK)







class Friend_Request_View(APIView):
    @swagger_auto_schema(tags=['Match'],responses={200: openapi.Response('ok', FriendshipInfoSerializer)})
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        querylist = FriendshipRequest.objects.all()
        owner = request.user
        FR = querylist.filter(to_user=request.user)
        FR = FR.filter(accepted= False)
        serializer = FriendshipInfoSerializer(FR,many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)






class Add_Or_Reject_Friends(APIView):
    @swagger_auto_schema(tags=['Match'],responses={200: openapi.Response('ok')})
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        print(request.GET['verb'])
        verb  = request.GET['verb']
        username  = request.GET['username']
        print(request.data)
        n_f = get_object_or_404(User, username=username)
        owner = request.user

        if verb == "accept":
            FriendshipRequest.accept(owner, n_f)
            c = Conversation()
            c.save()
            c.members.add(owner,n_f)
            return Response(
                {"message":"let's start your conversation"},
                status=status.HTTP_200_OK
                )


        elif verb == "decline":
            FriendshipRequest.decline(owner, n_f)

            return Response(
                {"message":"request declined successfully"},
                status=status.HTTP_200_OK
                )

        return Response ({"message":"Bad Request"},
                status=status.HTTP_400_BAD_REQUEST
                )

# class Top_Music(GenericAPIView):
#     def get(self,request):
#         user =request.user
#         songs = user.music.all()
#         serializer_class = UserTopSongserialize(songs,many = True)
#         return Response(serializer_class.data)


class User_Top_Music(GenericAPIView, UpdateModelMixin):
    queryset = CustomUser.objects.all()
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
            access_token = ""

            token_info = sp_oauth.get_cached_token(request)

            print ("Found cached token!")
            access_token = token_info['access_token']
            dict = {}
            list = []
            if access_token:
                user = get_object_or_404(self.queryset, pk=self.request.user.id)
                print ("Access token available! Wating for find your friends...")
                sp = spotipy.Spotify(access_token)
                results = sp.current_user_top_tracks(
                limit=50, offset=0)

                list_of_results = results["items"]

                list_of_artist_names = []
                list_of_song_names = []
                list_of_albums = []

                for result in list_of_results:
                    result["album"]
                    list_of_artist_names.append( result["artists"][0]["name"])
                    list_of_song_names.append(result["name"])
                    list_of_albums.append(result["album"]["name"])
                    dict["music_name "] = result["name"]
                    dict[" artist_name"] = result["artists"][0]["name"]
                    dict["album "] =  result["album"]["name"]
                    dict[" url"] = result["album"]["images"][2]['url']
                    list.append(dict)

            return Response(list)


class User_Top_Artist(GenericAPIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        access_token = ""

        token_info = sp_oauth.get_cached_token(request)

        print ("Found cached token!")
        access_token = token_info['access_token']

        if access_token:
            print ("Access token available! Wating for find your friends...")
            sp = spotipy.Spotify(access_token)
            results = sp.current_user_top_artists(limit=50, offset=0, time_range='medium_term')
            temp = []
            dict = {}
            for i in range(50):
                    url = "url"
                    name = "name"
                    dict[url] = results['items'][i]['images'][2]['url']
                    dict[name] = results['items'][i]['name']
                    temp.append(dict)
                    dict = {}

            return Response(temp)
        else:
            return Response("failed")
