from django.db import models

# model that store 6 of each user top song use this model in follower group
class Artist(models.Model):
    artist_id = models.CharField(max_length=250,null=True, blank=True)
    artist_name = models.CharField(max_length=250,null=True, blank=True)
    image_url = models.CharField(max_length=250,null=True, blank=True)
    spotify_url = models.CharField(max_length=250,null=True, blank=True)
    

# model that store information of user music interest such as music name artist and so on
class Music(models.Model):
    track_id = models.CharField(max_length=250,null=True, blank=True)
    track_name = models.CharField(max_length=250,null=True, blank=True)
    artist_name = models.CharField(max_length=250,null=True, blank=True)
    image_url = models.CharField(max_length=250,null=True, blank=True)
    spotify_url = models.CharField(max_length=250,null=True, blank=True)
    album = models.CharField(max_length=250,null=True, blank=True)
    