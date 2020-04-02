import hashlib, binascii, os
from music.models import User_top_music,Music
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


# class Music(models.Model):
class Friends(models.Model):
    username = models.CharField(_('username'), max_length=30, blank=True, unique=False)

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    FEMALE = 'Female'
    MALE = 'Male'

    TYPE_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    gender = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=MALE,
    )
    nickname = models.CharField(_('nickname'), max_length=30, blank=True, unique=False)
    email = models.EmailField(_('email address'), unique=True)
    birthdate = models.DateField(null=True)
    bio = models.CharField(_('biography'), max_length=150, blank=True, null=True)
    intersts = models.CharField(_('interests'), max_length=30, blank=True, null=True)
    user_avatar = models.ImageField(upload_to="images/", blank=True)
    spotify_token = models.CharField(_('spotify token'), max_length=220, blank=True, null=True)
    assigned = models.ForeignKey(Music, default=None, null=True,blank=True, on_delete=models.SET_NULL)
    friends = models.ManyToManyField(Friends)
    music = models.ManyToManyField(User_top_music)
    status = models.CharField(blank = True,max_length = 10)


    #location =
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['gender', 'email','password']
