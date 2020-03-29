from django.shortcuts import render,redirect
from django.http import HttpResponse
from account.models import CustomUser
from django.views.decorators.csrf import csrf_exempt


import os
import json
import sys
import spotipy
from spotipy import oauth2
import spotipy.util as util

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# os.environ['SPOTIPY_CLIENT_ID'] = cid
# os.environ['SPOTIPY_CLIENT_SECRET'] = secret
# os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/spotify/auth/'


SPOTIPY_CLIENT_ID = 'b086b316d65241c2b7a1ac4e2e797c91'
SPOTIPY_CLIENT_SECRET = '36cbb32cfe8c4ecbba50083ce277b1ab'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/spotify/auth/'
SCOPE = 'user-top-read'
CACHE = '.spotipyoauthcache'



sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)



class SpotifyView(APIView):

    @csrf_exempt
    @permission_classes([IsAuthenticated])
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
                print ("Access token available! Trying to get user information...")
                sp = spotipy.Spotify(access_token)
                results = sp.current_user()
                return Response(results)

            else:
                return getSPOauthURI()
        else:
            # print("here")
            return  Response( { 
               'message': 'Your are not logged in'
            },
                status=status.HTTP_401_UNAUTHORIZED
            )
   
