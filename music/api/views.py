from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

import os
import json
import sys
from account.models import CustomUser
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


class User_Top_Music(GenericAPIView, UpdateModelMixin):
    queryset = CustomUser.objects.all()
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
            access_token = ""

            token_info = sp_oauth.get_cached_token(request)

            print ("Found cached token!")
            access_token = token_info['access_token']

            if access_token:
                user = get_object_or_404(self.queryset, pk=self.request.user.id)
                print ("Access token available! Wating for find your friends...")
                sp = spotipy.Spotify(access_token)
                results = sp.current_user_top_tracks(
                limit=50, offset=0)
                for song in range(50):
                    list = []
                    list.append(results)
                    with open('top50_data.json', 'w', encoding='utf-8') as f:
                        json.dump(list, f, ensure_ascii=False, indent=4)

                with open('top50_data.json') as f:
                    data = json.load(f)
                list_of_results = data[0]["items"]

                list_of_artist_names = []
                list_of_song_names = []
                list_of_albums = []

                for result in list_of_results:
                    result["album"]
                    list_of_artist_names.append( result["artists"][0]["name"])
                    list_of_song_names.append(result["name"])
                    list_of_albums.append(result["album"]["name"])
                    music = User_top_music.objects.create(music_name = result["name"],artist_name =result["artists"][0]["name"],album = result["album"]["name"])
                    user.music.add(music)
                    user.save()
                    for mn,al,ar in User_top_music.objects.values_list('music_name','album','artist_name').distinct():
                                User_top_music.objects.filter(pk__in=User_top_music.objects.filter(music_name=mn,artist_name = ar,album = al).values_list('id', flat=True)[1:]).delete()
            list= []
            songs = user.music.all()
            for song in songs:
                serializer = UserTopSongserialize(song)
                list.append(serializer.data)

            return Response(list)
