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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from music.api.serializers import UserProfileSerializer

SPOTIPY_CLIENT_ID = 'c42e107d3ae641e4af9e08e7d7a55b9b'
SPOTIPY_CLIENT_SECRET = 'cd1e4e0aa3684e34ae12b313ebea1074'
SPOTIPY_REDIRECT_URI = 'http://localhost:3000/spotifyresult/'
COPE = 'user-top-read user-read-currently-playing user-read-playback-state user-library-read'
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
            print ("Found cached token!")
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
   
class Find_friends(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):

        access_token = ""

        token_info = sp_oauth.get_cached_token(request)

        # if token_info:
        print ("Found cached token!")
        access_token = token_info['access_token']
        # else:
        #     url = request.build_absolute_uri()
        #     code = sp_oauth.parse_response_code(url)
            # if code:
            #     print ("Found Spotify auth code in Request URL! Trying to get valid access token...")
            #     token_info = sp_oauth.get_access_token(code,request=request)
            #     access_token = token_info['access_token']

        if access_token:
            print ("Access token available! Wating for find your friends...")
            sp = spotipy.Spotify(access_token)
            friends(request,request.user.id,sp)
            total_dict = {}
            total_dict["FEMALE"] = friends.dataFE
            total_dict["MALE"] = friends.dataM
            return JsonResponse(total_dict, safe=False)



class Match(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
                dataM = {}
                dataFE = {}
                activeuser = CustomUser.objects.get(id = request.user.id)
                users = activeuser.friends.all()
                for friend in users:
                    if friend.gender == "Male":
                        dataM[friend.username] = friend.nickname
                    else:
                        dataFE[user.username] = friend.nickname

                total_dict = {}
                total_dict["FEMALE"] = dataFE
                total_dict["MALE"] = dataM
                return JsonResponse(total_dict, safe=False)

