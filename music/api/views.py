from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from account.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse


import os
import json
import sys
import spotipy
from spotipy import oauth2
import spotipy.util as util

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from music.api.serializers import UserProfileSerializer

from music.views import friends

# os.environ['SPOTIPY_CLIENT_ID'] = cid
# os.environ['SPOTIPY_CLIENT_SECRET'] = secret
# os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/spotify/auth/'


SPOTIPY_CLIENT_ID = '8167c1d1f43643e989ae8f5b427205c7'
SPOTIPY_CLIENT_SECRET = '2b506c6b41da420c80dc242916f9ac69'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify/auth/'
SCOPE = 'user-top-read user-read-currently-playing user-read-playback-state user-library-read'
CACHE = '.spotipyoauthcache'



sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)



class SpotifyView(APIView):
    @csrf_exempt
    def get(self, request):
        if request.user.is_authenticated :
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
                print ("Access token available! Trying to get user information...            "+ access_token)
                sp = spotipy.Spotify(access_token)
                results = sp.current_user()
                print(access_token + " access_token    ")
                return Response(results)

            else:
                return getSPOauthURI()
        else:
            # print("here")
            return  Response( {
               'message': 'Your are not logged in'
            },
                status=status.HTTP_400_BAD_REQUEST
            )

class Find_friends(APIView):
    @csrf_exempt
    def get(self, request):
        if request.user.is_authenticated :
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
                print ("Access token available! Wating for find your friends...")
                sp = spotipy.Spotify(access_token)
                friends(request,request.user.id,sp)
                total_dict = {}
                total_dict["FEMALE"] = friends.dataFE
                total_dict["MALE"] = friends.dataM
                return JsonResponse(total_dict, safe=False)


            else:
                return getSPOauthURI()
        else:
            return  Response( {
               'message': 'Your are not logged in'
            },
                status=status.HTTP_400_BAD_REQUEST
            )




class Match(APIView):
    @csrf_exempt
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
