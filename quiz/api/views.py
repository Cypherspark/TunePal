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
from quiz.api.serializers import *
from quiz.models import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

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
                    limit=5, offset=0)
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

                            question = "the song with name "+result["name"]+" is for ...."
                            list = random.sample(temp, len(temp))
                            choices2 = list[0]
                            choices3 = list[1]
                            choices4 = list[2]
                            list.append(result["artists"][0]["name"])
                            answer = result["artists"][0]["name"]
                            choices = random.sample(list,4)
                            temp.append(result["artists"][0]["name"])
                            Quiz1 = QuizPassage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)
                            for quiz in QuizPassage.objects.values_list('question', flat=True).distinct():
                                        QuizPassage.objects.filter(pk__in=QuizPassage.objects.filter(question=quiz).values_list('id', flat=True)[1:]).delete()

                    results = sp.current_user_top_artists(limit=5, offset=0, time_range='medium_term')
                    for i in range(len(results['items'])):
                        if results['items'][i]['name'] not in temp:
                            temp.append(results['items'][i]['name'])

                    for i in range(len(results['items'])):

                            if results['items'][i]['name'] in temp:
                                temp.remove(results['items'][i]['name'])
                            question = results['items'][i]['images'][2]['url']
                            list = random.sample(temp, 3)
                            list.append(results['items'][i]['name'])
                            answer = results['items'][i]['name']
                            choices = random.sample(list,4)
                            temp.append(results['items'][i]['name'])
                            Quiz1 = QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)
                            for quiz in QuizImage.objects.values_list('question', flat=True).distinct():
                                        QuizImage.objects.filter(pk__in=QuizImage.objects.filter(question=quiz).values_list('id', flat=True)[1:]).delete()

                    return Response({
                    "question maked"
                    })


                else:
                        return  Response( {
                           'message': 'Your are not logged in'
                        },
                            status=status.HTTP_400_BAD_REQUEST
                        )


class Imagequiz(GenericAPIView):
    queryset = QuizImage.objects.all()
    list1=list(queryset)
    def get(self,request):
        questions = []
        random.seed()
        question = random.choice(self.list1)
        serializer = Imagequizserializer(question)
        questions.append(serializer.data)
        return Response(questions)
class passagequiz(GenericAPIView):
    queryset = QuizPassage.objects.all()
    list1=list(queryset)
    def get(self,request):
        questions = []
        question = random.choice(self.list1)
        serializer = passagequizserializer(question)
        questions.append(serializer.data)
        return Response(questions)
class checkimageanswer(GenericAPIView):
     anser_list = []
     queryset = QuizImage.objects.all()
     serializer_class = Checkimagequiz
     def post(self,request):
        user = get_object_or_404(CustomUser,pk =self.request.user.id)
        quiz = get_object_or_404(self.queryset,id=int(request.data.get('quiz_id')))
        answer = request.POST.get('answer')
        if quiz.answer == answer:
            score = user.score
            score = int(score)
            score+= 10
            user.score = score
            user.save()
            return Response(quiz.answer)
        else:
            return Response(quiz.answer)
class checkpssageanswer(GenericAPIView):
     anser_list = []
     queryset = QuizPassage.objects.all()
     serializer_class = Checkpassagequiz
     def post(self,request):
        user = get_object_or_404(CustomUser,pk =self.request.user.id)
        print(request.data.get('quiz_id'))
        quiz = get_object_or_404(self.queryset,id=int(request.data.get('quiz_id')))
        answer = request.POST.get('answer')
        if quiz.answer == answer:
            score = user.score
            score = int(score)
            score+= 10
            user.score = score
            user.save()
            return Response(quiz.answer)

        else:
            return Response(quiz.answer)

class getscore(GenericAPIView):
        def get(self,request):
            user = get_object_or_404(CustomUser,pk =self.request.user.id)
            serializer = UserScore(user)
            return Response(serializer.data)
