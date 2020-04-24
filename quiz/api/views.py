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
import csv

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
        print ("Found cached token!")
        token_info = sp_oauth.get_cached_token(request)
        access_token = token_info['access_token']
        dict = {}
        q = []
        if access_token:
                    print ("Access token available! Wating for find question...")
                    sp = spotipy.Spotify(access_token)
                    QuizImage.objects.all().delete()
                    queryset = User_top_music.objects.all()
                    serializer_class = UserTopSongserialize(queryset,many = True)
                    artist = []
                    for i in range(len(serializer_class.data)):
                        if serializer_class.data[i]['artist_name'] not in artist:
                                artist.append(serializer_class.data[i]['artist_name'])
                    song = []
                    for i in range(len(serializer_class.data)):
                        if serializer_class.data[i]['music_name'] not in song:
                                song.append(serializer_class.data[i]['music_name'])
                    album = []
                    for i in range(len(serializer_class.data)):
                        if serializer_class.data[i]['album'] not in album:
                                album.append(serializer_class.data[i]['album'])
                    for i in range(int(len(serializer_class.data)/2)):
                            if serializer_class.data[i]['artist_name'] in artist:
                                artist.remove(serializer_class.data[i]['artist_name'])

                            question =serializer_class.data[i]['music_name']+" is for .... , "+" https://onesoftwaresolution.com/wp-content/uploads/2017/01/iStock-147246163-900x500.jpg"
                            list = random.sample(artist,3)
                            choices2 = list[0]
                            choices3 = list[1]
                            choices4 = list[2]
                            list.append(serializer_class.data[i]['artist_name'])
                            answer = serializer_class.data[i]['artist_name']
                            choices = random.sample(list,4)
                            artist.append(serializer_class.data[i]['artist_name'])
                            quiz1 =QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)
                            for quiz in QuizImage.objects.values_list('question', flat=True).distinct():
                                                QuizImage.objects.filter(pk__in=QuizImage.objects.filter(question=quiz).values_list('id', flat=True)[1:]).delete()
                    #
                    for i in range(int(len(serializer_class.data)/2)):
                            if serializer_class.data[i]['artist_name'] in artist:
                                artist.remove(serializer_class.data[i]['artist_name'])

                            question ="front image is related to .... , "+serializer_class.data[i]['genre']
                            list = random.sample(artist,3)
                            choices2 = list[0]
                            choices3 = list[1]
                            choices4 = list[2]
                            list.append(serializer_class.data[i]['artist_name'])
                            answer = serializer_class.data[i]['artist_name']
                            choices = random.sample(list,4)
                            artist.append(serializer_class.data[i]['artist_name'])
                            quiz1 =QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)
                            for quiz in QuizImage.objects.values_list('question', flat=True).distinct():
                                                QuizImage.objects.filter(pk__in=QuizImage.objects.filter(question=quiz).values_list('id', flat=True)[1:]).delete()


                    res = sp.playlist('0MG9jIyagfVWDLhShEhvbg', fields=None, market=None)
                    artist = []

                    for i in range(len(res['tracks']['items'])):
                        if res['tracks']['items'][i]['track']['album']['artists'][0]['name'] not in artist:
                                artist.append(res['tracks']['items'][i]['track']['album']['artists'][0]['name'])

                    so = []
                    for i in range(len(res['tracks']['items'])):
                                so.append(res['tracks']['items'][i]['track']['name'])
                    album =  ['Kind of Blue','Elvis Presley ',"Here's Little Richard ","Kid A","Lemonade","I Dreamed a Dream","Meteora",
                    "Metro Station","Higher Love","Roses","Snacks","Recovery","Euphoria (Standard US/Latin version)","Young, Wild & Free (feat. Bruno Mars)",
                    "Stronger (Deluxe Version)","Nothing but the Beat (Ultimate Edition)","My Beautiful Dark Twisted Fantasy","Sorry For Party Rocking (Deluxe Version)"
                    ,"Rolling Papers","Stereo Love","The Papercut Chronicles II","The Sequel (Deluxe)",
                    "Whatever","Black And Yellow","Born This Way","Lasers","Femme Fatale (Deluxe Version)","Torches","LOVE? (Deluxe Edition)","Singles"
                    ,"Doo-Wops & Hooligans","Planet Pit (Deluxe Version)","The Kickback","Only By The Night","I AM...SASHA FIERCE",
                    "The Time Of Our Lives (Canadian Version)","Fearless","The Blueprint 3","Only One Flo (Part 1)","Girls Night Out","The Fame Monster (Deluxe Edition)"
                    ,"Ocean Eyes","THE E.N.D. (THE ENERGY NEVER DIES)","Replay","Believe (Deluxe Edition)","Up All Night","Avril Lavigne","Badlands","Bamboleo single","Believer(feat.Lil Wayne) Single","Colors Single","Divide(Deluxe)"]
                    # # for i in range(len(res['tracks']['items'])):
                    # #     if res['tracks']['items'][i]['track']['album']['name'] not in album:
                    # #             album.append(res['tracks']['items'][i]['track']['album']['name'])
                    list1 = []

                    with open('quiz//api//song.csv', newline='') as csvfile:
                         spamreader = csv.reader(csvfile, quotechar=',')
                         for row in spamreader:
                             list1.append(row)
                    del list1[0]
                    del list1[0]
                    del list1[73]

                    song = []
                    for x in list1 :
                        if x[2] not in artist:
                            track = x[1]
                            track = track.replace('"','')
                            str_artist = x[2]
                            str_artist = str_artist.replace('"','')
                            if track not in so:
                                song.append(track)
                            if str_artist not in artist:
                                artist.append(str_artist)

                    # for i in range(len(res['tracks']['items'])):
                    #     print('artist_name : '+res['tracks']['items'][i]['track']['album']['artists'][0]['name']+ "  trackname : "+res['tracks']['items'][i]['track']['name']+"‌  album :"+ res['tracks']['items'][i]['track']['album']['name'] )
                    #     artist_name = "artist_name"
                    #     music_name = "music_name"
                    #     album = "album"
                    #     url = "url"
                    #     dict[artist_name] = res['tracks']['items'][i]['track']['album']['artists'][0]['name']
                    #     dict[music_name] = res['tracks']['items'][i]['track']['name']
                    #     dict[album] = res['tracks']['items'][i]['track']['album']['name']
                    #     dict[url] = res['tracks']['items'][i]['track']['album']['images'][2]['url']
                    #     q.append(dict)
                    for i in range(len(res['tracks']['items'])):
                            if res['tracks']['items'][i]['track']['album']['artists'][0]['name'] in artist:
                                artist.remove(res['tracks']['items'][i]['track']['album']['artists'][0]['name'])
                            question = "The song with name ( "+res['tracks']['items'][i]['track']['name']+" ) is for .... , "+"https://onesoftwaresolution.com/wp-content/uploads/2017/01/iStock-147246163-900x500.jpg"
                            list = random.sample(artist, 3)
                            list.append(res['tracks']['items'][i]['track']['album']['artists'][0]['name'])
                            answer = res['tracks']['items'][i]['track']['album']['artists'][0]['name']
                            choices = random.sample(list,4)
                            artist.append(res['tracks']['items'][i]['track']['album']['artists'][0]['name'])
                            quiz1 =QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)


                    for i in range(len(res['tracks']['items'])):
                            if res['tracks']['items'][i]['track']['album']['artists'][0]['name'] in artist:
                                artist.remove(res['tracks']['items'][i]['track']['album']['artists'][0]['name'])
                            question = "The album with name ("+res['tracks']['items'][i]['track']['album']['name']+") and front image is for .... , "+res['tracks']['items'][i]['track']['album']['images'][2]['url']
                            list = random.sample(artist, 3)
                            list.append(res['tracks']['items'][i]['track']['album']['artists'][0]['name'])
                            answer = res['tracks']['items'][i]['track']['album']['artists'][0]['name']
                            choices = random.sample(list,4)
                            artist.append(res['tracks']['items'][i]['track']['album']['artists'][0]['name'])
                            QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)

                    for i in range(len(res['tracks']['items'])):
                            indexes = [index for index in range(len(artist)) if artist[index] == res['tracks']['items'][i]['track']['album']['artists'][0]['name'] ]
                            if res['tracks']['items'][i]['track']['name'] in song:
                                    song.remove(res['tracks']['items'][i]['track']['name'])

                            question = "Which one of this songs is for  ("+res['tracks']['items'][i]['track']['album']['artists'][0]['name']+" "+") , https://onesoftwaresolution.com/wp-content/uploads/2017/01/iStock-147246163-900x500.jpg"
                            list = random.sample(song, 3)
                            list.append(res['tracks']['items'][i]['track']['name'])
                            answer = res['tracks']['items'][i]['track']['name']
                            choices = random.sample(list,4)
                            quiz1 =QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)

                    for i in range(len(res['tracks']['items'])):
                          if res['tracks']['items'][i]['track']['album']['name'] in album:
                                  album.remove(res['tracks']['items'][i]['track']['album']['name'])
                          question = "Which one of this albums is for  ("+res['tracks']['items'][i]['track']['album']['artists'][0]['name']+") , https://onesoftwaresolution.com/wp-content/uploads/2017/01/iStock-147246163-900x500.jpg"
                          list = random.sample(album, 3)
                          list.append(res['tracks']['items'][i]['track']['album']['name'])
                          answer = res['tracks']['items'][i]['track']['album']['name']
                          choices = random.sample(list,4)
                          album.append(res['tracks']['items'][i]['track']['album']['name'])
                          quiz1 = QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)

                    for i in range(len(res['tracks']['items'])):
                          if res['tracks']['items'][i]['track']['name'] in song:
                                  song.remove(res['tracks']['items'][i]['track']['name'])
                          question = "Which one of this songs is in the album with name ( "+res['tracks']['items'][i]['track']['album']['name']+" ) and front image , "+res['tracks']['items'][i]['track']['album']['images'][2]['url']
                          list = random.sample(song, 3)
                          list.append(res['tracks']['items'][i]['track']['name'])
                          answer = res['tracks']['items'][i]['track']['name']
                          choices = random.sample(list,4)
                          quiz1 =QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)

                    for i in range(len(res['tracks']['items'])):
                          if res['tracks']['items'][i]['track']['album']['name'] in album:
                                  album.remove(res['tracks']['items'][i]['track']['album']['name'])
                          question = "the song  with name ( "+res['tracks']['items'][i]['track']['name']+" ) is in which one of this albums"+" , https://onesoftwaresolution.com/wp-content/uploads/2017/01/iStock-147246163-900x500.jpg"
                          list = random.sample(album, 3)
                          list.append(res['tracks']['items'][i]['track']['album']['name'])
                          answer = res['tracks']['items'][i]['track']['album']['name']
                          choices = random.sample(list,4)
                          album.append(res['tracks']['items'][i]['track']['album']['name'])
                          quiz1 =QuizImage.objects.create(question = question,choices1 = choices[0],choices2 = choices[1] , choices3 = choices[2],choices4 = choices[3] , answer = answer)
                    for quiz in QuizImage.objects.values_list('question', flat=True).distinct():
                                QuizImage.objects.filter(pk__in=QuizImage.objects.filter(question=quiz).values_list('id', flat=True)[1:]).delete()
                    quiz = QuizImage.objects.all()
                    serializer = Imagequizserializer(quiz,many = True)
                    return Response(serializer.data)




class quiz(GenericAPIView):
    queryset = QuizImage.objects.all()
    list1=list(queryset)
    def get(self,request):
        questions = []
        random.seed()
        question = random.choice(self.list1)
        i = 0;
        while question.quiz_id == "show" and i< len(self.list1)-1:
            question = random.choice(self.list1)
            i+=1
            if i == len(self.list1)-1:
                for q in QuizImage.objects.all():
                    q.quiz_id == ""
                    i = 0;
                    question.quiz_id = ""
        question.quiz_id = "show"
        serializer = Imagequizserializer(question)
        questions.append(serializer.data)
        return Response(questions)

class checkanswer(GenericAPIView):
     dict = {}
     queryset = QuizImage.objects.all()
     serializer_class = Checkanswer
     def post(self,request):
        user = get_object_or_404(CustomUser,pk =self.request.user.id)
        quiz = get_object_or_404(self.queryset,id=int(request.data.get('quiz_id')))
        answer = request.data.get('answer')
        if quiz.answer == answer:
            score = user.score
            score = int(score)
            score+= 10
            user.score = score
            user.save()
            self.dict['answer'] = quiz.answer
            self.dict['score'] = user.score
            return Response(dict)

        else:
            self.dict['answer'] = quiz.answer
            self.dict['score'] = user.score
            return Response(self.dict)


class getscore(GenericAPIView):
        def get(self,request):
            user = get_object_or_404(CustomUser,pk =self.request.user.id)
            serializer = UserScore(user)
            return Response(serializer.data)
