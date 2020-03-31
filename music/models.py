from django.db import models

class User_top_music(models.Model):
    music_name = models.CharField(max_length=250)
    artist_name = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    album = models.CharField(max_length=250)
    music_id = models.CharField(max_length=250)
