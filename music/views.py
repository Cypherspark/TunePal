from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from account.models import CustomUser,Music,Friend
from django.http import HttpResponse
from music.models import User_top_music
import sys
import spotipy
import spotipy.util as util
from django.shortcuts import get_object_or_404
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
from django.http import JsonResponse

def counting(list):
   n = len(list)
   tempcount = []
   tempcval = []
   for next in list:
      if next in tempcval:
         point = tempcval.index(next)
         tempcount[point] = tempcount[point] + 1
      else:
         tempcval.append(next)
         tempcount.append(1)

   maxCount = max(tempcount)
   point = tempcount.index(maxCount)

   return tempcval[point]
def matchoptions(request,id,sp):
            results = sp.current_user_playing_track()
            if results != None:
                musics = Music.objects.all()
                user = get_object_or_404(CustomUser,id =id)
                for music in musics:
                    if music.id == CustomUser.assigned_id:
                        Music.objects.filter(id=music.id).delete()
                user = get_object_or_404(CustomUser,id =id)
                music = Music.objects.create(music_name=results['item']['name'],artist_name = results['item']['album']['artists'][0]['name'],album =  results['item']['album']['name'])
                user.assigned_id = music.id
                user.save()
            else :
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
                # search in fifty of top song
                for result in list_of_results:
                    result["album"]
                    list_of_song_names.append(result["name"])
                    list_of_albums.append(result["album"]["name"])

                TopArtist = sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')
                Album = counting(list_of_albums)
                Song = counting(list_of_song_names)
                Artist = TopArtist['items'][0]['name']

                musics = Music.objects.all()
                user = get_object_or_404(CustomUser,id =id)
                # give just 5 of top song
                store_song = sp.current_user_top_tracks(
                    limit=5, offset=0)
                user.music.all().delete()
                for song in store_song :
                    song = User_top_music.objects.create(music_name=[result["name"]],artist_name = result["name"],album = result["album"]["name"],music_id = result['id'])
                    user.music.add(song)

                for music in musics:
                    if music.id == user.assigned_id:
                        Music.objects.filter(id=music.id).delete()
                music = Music.objects.create(music_name=Song,artist_name = Artist,album = Album)
                user.assigned_id = music.id
                user.save()

def friends(request,id,sp):
    matchoptions(request,id,sp)
    users = CustomUser.objects.all()
    Activeuser = get_object_or_404(CustomUser,id =id)
    task =Activeuser.assigned

    a=0
    friends.dataM = {}
    friends.dataFE = {}
    for user in users:
        if user.assigned != None and task !=None:
         if user.username != Activeuser.username:
            if task.music_name == user.assigned.music_name:
                a+=1
            if Activeuser.assigned.album == user.assigned.album:
                a+=1
            if Activeuser.assigned.artist_name == user.assigned.artist_name:
                a+=1
            persent = (a*100)/3
            if persent>30:
                if user.gender == 'Male':
                    friends.dataM[user.username] = user.nickname
                else:
                    friends.dataFE[user.username] = user.nickname
                # check if a user is valid don't add again
                flag = Activeuser.friends.filter(username = user.username)
                if flag:
                    pass
                else:
                     f= Friend.objects.create(username = user.username,nickname = user.nickname,gender = user.gender,spotify_token = user.spotify_token)
                     Activeuser.friends.add(f)
