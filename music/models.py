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
class Quiz(models.Model):
    question = models.CharField(max_length=500)
    choices1 = models.CharField(max_length = 20)
    choices2 = models.CharField(max_length = 20)
    choices3 = models.CharField(max_length = 20)
    choices4 = models.CharField(max_length = 20, default = None)
    answer = models.CharField(max_length = 20)
    quiz_id = models.CharField(max_length = 200000000000000000000,blank=True,null = True,default = None)
