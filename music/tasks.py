from celery import shared_task
from music.models import Music, Artist
from account.models import CustomUser
from django.shortcuts import get_object_or_404


@shared_task
# do some heavy stuff
def save_songs(list_of_results, user_id):
    user = get_object_or_404(CustomUser, pk = user_id)
    for result in list_of_results:
        dict = {}
        result["album"]
        dict["track_name"] = result["name"]
        dict["artist_name"] = result["artists"][0]["name"]
        dict["album"] =  result["album"]["name"]
        dict["image_url"] = result["album"]["images"][2]['url']
        dict["spotify_url"] = result["external_urls"]["spotify"]
        music, created = Music.objects.get_or_create(**dict)
        user.tracks.add(music)