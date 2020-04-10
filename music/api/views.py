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
        print("sdoubgjsl")
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

class Find_friends(APIView):
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
            friends(request,request.user.id,sp)
            total_dict = {}
            total_dict["FEMALE"] = friends.dataFE
            total_dict["MALE"] = friends.dataM
            return JsonResponse(total_dict, safe=False)



class Match(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request):
        dataM = []
        dataFE = []
        activeuser = CustomUser.objects.get(id = request.user.id)
        print(activeuser.id)
        users = activeuser.friends.all()
        for friend in users:
            friendserialized = FriendInfoSerializer(friend)
            dataM.append(friendserialized.data)


        total_dict = {}
        total_dict["FEMALE"] = dataFE
        total_dict["MALE"] = dataM
        return JsonResponse(total_dict, safe=False)
class UserUpdateScore(GenericAPIView,UpdateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileUpdateScore
    def put(self, request):
        print(request.user.id)
        question = get_object_or_404(CustomUser, pk=request.user.id)
        serializer = UserProfileUpdateScore(question, data=request.data, partial=True)
        if serializer.is_valid():
            print("dsuogdsiuohiodshfo")
            question = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
             if request.method == 'GET':
                 queryset = CustomUser.objects.all()
                 serializer = UserProfileUpdateScore(queryset, many=True)
                 return Response(serializer.data)
class User_Top_Music(GenericAPIView, UpdateModelMixin):
    queryset = CustomUser.objects.all()
    def get(self, request):
        list= []
        user = get_object_or_404(self.queryset, pk=self.request.user.id)
        songs = user.music.all()
        for song in songs:
            serializer = UserTopSongserialize(song)
            list.append(serializer.data)

        return Response(list)

class question(APIView):
    @csrf_exempt
    def get(self, request):
                access_token = ""

                token_info = sp_oauth.get_cached_token(request)

                print ("Found cached token!")
                access_token = token_info['access_token']

                if access_token:
                    print ("Access token available! Wating for find your friends...")
                    sp = spotipy.Spotify(access_token)
                    results = sp.current_user_top_tracks(
                    limit=10, offset=0)
                    for song in range(50):
                        list = []
                        list.append(results)
                        with open('top50_data.json', 'w', encoding='utf-8') as f:
                            json.dump(list, f, ensure_ascii=False, indent=4)

                    with open('top50_data.json') as f:
                        data = json.load(f)
                    list_of_results = data[0]["items"]
                    list_of_artist_names=[]
                    for result in list_of_results:
                            result["album"]
                            list_of_artist_names.append( result["artists"][0]["name"])
                    temp = []
                    for x in list_of_artist_names:
                        if x not in temp:
                            temp.append(x)

                    for result in list_of_results:
                            result["album"]
                            if result["artists"][0]["name"] in temp:
                                temp.remove(result["artists"][0]["name"])

                            print(temp)
                            question = "the song with name "+result["name"]+"is for ...."
                            list = random.sample(temp, len(temp))
                            choices2 = list[0]
                            choices3 = list[1]
                            choices4 = list[2]
                            list.append(result["artists"][0]["name"])
                            answer = result["artists"][0]["name"]
                            choices = random.sample(list,4)
                            temp.append(result["artists"][0]["name"])
                            # print(choices)
                            Quiz1 = Quiz.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)
                            Activeuser = get_object_or_404(CustomUser,id =request.user.id)
                            Activeuser.quiz.add(Quiz1)

                    results = sp.current_user_top_artists(limit=10, offset=0, time_range='medium_term')

                    for i in range(len(results)):
                            if results['items'][i]['name'] in temp:
                                temp.remove(results['items'][i]['name'])

                            print(temp)
                            question = results['items'][i]['images'][2]['url']
                            print(temp)
                            list = random.sample(temp, 3)
                            list.append(results['items'][i]['name'])
                            answer = results['items'][i]['name']
                            choices = random.sample(list,4)
                            temp.append(results['items'][i]['name'])
                            Quiz1 = Quiz.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)
                            Activeuser = get_object_or_404(CustomUser,id =request.user.id)
                            Activeuser.quiz.add(Quiz1)
                            for quiz in Quiz.objects.values_list('question', flat=True).distinct():
                                        Quiz.objects.filter(pk__in=Quiz.objects.filter(question=quiz).values_list('id', flat=True)[1:]).delete()

                    return Response(results)


                else:
                        return  Response( {
                           'message': 'Your are not logged in'
                        },
                            status=status.HTTP_400_BAD_REQUEST
                        )
class quiz(GenericAPIView):
    queryset = CustomUser.objects.all()
    def get(self, request):
        list= []
        user = get_object_or_404(self.queryset, pk=self.request.user.id)
        songs = user.quiz.all()
        for song in songs:
            serializer = Userprivatequiz(song)
            list.append(serializer.data)
        return Response(list)
