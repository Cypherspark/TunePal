import hashlib, binascii, os
from music.models import User_top_music,Music
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class UserLocation(models.Model):
    latitude = models.FloatField(_("latitude"),null=True, blank=True)
    longitude = models.FloatField(_("longitude"),null=True, blank=True)
    country = models.CharField(_("country"),max_length=30, blank=True, unique=False)
    province = models.CharField(_("province"),max_length=30, blank=True, unique=False)
    neighbourhood = models.CharField(_("neighbourhood"),max_length=30, blank=True, unique=False)


# class Interests(models.Model):
#     title = models.CharField(_('title'), max_length=30, blank=True, null=True)

#     def __str__(self):
#         return title


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
    biography = models.CharField(_('biography'), max_length=150, blank=True, null=True)
    interests = models.CharField(_('interests'), max_length=30, blank=True, null=True)
    user_avatar = models.ImageField(upload_to="images/", blank=True)
    spotify_token = models.CharField(_('spotify token'), max_length=700, blank=True, null=True)
    assigned = models.ForeignKey(Music, default=None, null=True,blank=True, on_delete=models.SET_NULL)
    music = models.ManyToManyField(User_top_music,blank=True)
    status = models.CharField(blank = True,max_length = 10)
    
    location = models.OneToOneField(UserLocation,
                    blank=True,
                    null=True,
                    verbose_name=_("location"),
                    on_delete=models.CASCADE
                    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['gender', 'email','password']


class Friend(models.Model):
    users = models.ManyToManyField(CustomUser)
    current_user = models.ForeignKey(CustomUser, related_name="owner", null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend)

    def __str__(self):
        return str(self.current_user)