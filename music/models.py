from django.db import models

# model that store 6 of each user top song use this model in follower group
class User_top_music(models.Model):
    music_name = models.CharField(max_length=250)
    artist_name = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    album = models.CharField(max_length=250)
    music_id = models.CharField(max_length=250)

# model that store information of user music interest such as music name artist and so on
class Music(models.Model):
    music_name = models.CharField(max_length=250)
    artist_name = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    album = models.CharField(max_length=250)
