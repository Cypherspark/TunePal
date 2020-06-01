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
from music.tasks import save_songs


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

from celery import Celery, current_app

import random

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from TunePal.settings import EMAIL_HOST_USER


SPOTIPY_CLIENT_ID = 'c42e107d3ae641e4af9e08e7d7a55b9b'
SPOTIPY_CLIENT_SECRET = 'cd1e4e0aa3684e34ae12b313ebea1074'
SPOTIPY_REDIRECT_URI = 'https://mytunepal.ir/spotifyresult/'
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
        user = request.user
        user_id = user.id
        token_info = sp_oauth.get_cached_token(user_id)
        if token_info:
            access_token = token_info['access_token']
        else:
            url = request.build_absolute_uri()
            code = sp_oauth.parse_response_code(url)
            if code:
                print ("Found Spotify auth code in Request URL! Trying to get valid access token...")
                token_info = sp_oauth.get_access_token(code,user_id=user_id)
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
            try:
                random.seed()
                slist = random.sample(list(User.objects.exclude(id = request.user.id)),4)
                suggetionlist = Suggest(s_current_user = request.user)
                suggetionlist.save()
                suggetionlist.s_users.add(*slist)
            except:
                return Response(
                    {"message":"not enough users"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )


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
        if not FriendshipRequest.objects.filter(to_user=n_f, from_user=owner).exists():
            FR = FriendshipRequest(from_user=owner, to_user=n_f)
            FR.save()
            subject = "TunePal - New Request"
            SendEmail(request,str(n_f.email),"friend.html",n_f.username,owner.username,subject)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)







class Friend_Request_View(APIView):
    @swagger_auto_schema(tags=['Match'],responses={200: openapi.Response('ok', FriendshipInfoSerializer)})
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        owner = request.user
        querylist = FriendshipRequest.objects.filter(to_user = owner)
        FR = querylist.filter(accepted= False)
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
            subject = "TunePal - Request Result"
            SendEmail(request,str(n_f.email),"accept.html",n_f.username,owner.username,subject)
            FriendshipRequest.accept(owner, n_f)
            if not Conversation.objects.filter(members__in=[owner.id, n_f.id]).exists():
                if CustomUser.objects.filter(id = n_f.id).exists():
                    c = Conversation()
                    c.save()
                    c.members.add(owner,n_f)
                else:
                    return Response ({"message":"Bad Request"},
                            status=status.HTTP_400_BAD_REQUEST
                            )
            return Response(
                {"message":"let's start your conversation"},
                status=status.HTTP_200_OK
                )


        elif verb == "decline":
            subject = "TunePal - Request Result"
            SendEmail(request,str(n_f.email),"decline.html",n_f.username,owner.username,subject)
            FriendshipRequest.decline(owner, n_f)

            return Response(
                {"message":"request declined successfully"},
                status=status.HTTP_200_OK
                )

        return Response ({"message":"Bad Request"},
                status=status.HTTP_400_BAD_REQUEST
                )

class User_Top_Music(GenericAPIView, UpdateModelMixin):
    queryset = CustomUser.objects.all()
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        context = {}
        if 'username' not in request.GET.keys():
            user = request.user
        else:
            user = get_object_or_404(CustomUser, username = request.GET['username'])
        user_id = user.id
        # if user.tracks.exists():
        #     songs = user.tracks.all()
        #     serializer_class = UserTopSongserialize(songs,many = True)
        #     return Response(serializer_class.data)



        access_token = ""
        try:
            token_info = sp_oauth.get_cached_token(user_id=user_id)
            access_token = token_info['access_token']
            print ("Found cached token!")
            list = []
            if access_token:
                sp = spotipy.Spotify(access_token)
                results = sp.current_user_top_tracks(
                limit=50, offset=0)

                list_of_results = results["items"]
                list_of_artist_names = []
                list_of_song_names = []
                list_of_albums = []

                # task = save_songs.delay(list_of_results, request.user.id)
                # context['task_id'] = task.id
                # context['task_status'] = task.status

                for result in list_of_results:
                    dict = {}
                    result["album"]
                    list_of_artist_names.append( result["artists"][0]["name"])
                    list_of_song_names.append(result["name"])
                    list_of_albums.append(result["album"]["name"])
                    dict["track_name"] = result["name"]
                    dict["artist_name"] = result["artists"][0]["name"]
                    dict["album"] =  result["album"]["name"]
                    dict["image_url"] = result["album"]["images"][0]['url']
                    dict["spotify_url"] = result["external_urls"]["spotify"]
                    dict["preview_url"] = result["preview_url"]
                    if dict != {}:
                        list.append(dict)
                list.append(context)
            return Response(list)
        except:
            return Response({
                        'message': 'token not found'
                    },
                    status=status.HTTP_404_NOT_FOUND)


class User_Top_Artist(GenericAPIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        access_token = ""
        if 'username' not in request.GET.keys():
            user = request.user
        else:
            user = get_object_or_404(CustomUser, username = request.GET['username'])
        user_id = user.id
        token_info = sp_oauth.get_cached_token(user_id)

        try:
            access_token = token_info['access_token']

            if access_token:
                sp = spotipy.Spotify(access_token)
                results = sp.current_user_top_artists(limit=50, offset=0, time_range='medium_term')
                list_of_results = results['items']
                temp = []
                for result in list_of_results:
                    dict = {}
                    dict["artist_name"] = result["name"]
                    dict["image_url"] = result['images'][0]['url']
                    dict["spotify_url"] = result['external_urls']["spotify"]
                    if dict != {}:
                        temp.append(dict)

                return Response(temp)
            else:
                return Response("failed")
        except:
            return Response({
                        'message': 'token not found'
                    },
                    status=status.HTTP_404_NOT_FOUND)



class TaskView(APIView):
    def get(self, request):
        task_id = request.GET['task_id']
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)
