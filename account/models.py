import hashlib, binascii, os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class UserLocation(models.Model):
    latitude = models.FloatField(_("latitude"),null=True, blank=True)
    longitude = models.FloatField(_("longitude"),null=True, blank=True)
    country = models.CharField(_("country"),max_length=30, blank=True, unique=False)
    province = models.CharField(_("province"),max_length=30, blank=True, unique=False)
    neighbourhood = models.CharField(_("neighbourhood"),max_length=30, blank=True, unique=False)


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
    
    location = models.OneToOneField(UserLocation,
                    blank=True,
                    null=True,
                    verbose_name=_("location"),
                    on_delete=models.CASCADE
                    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['gender', 'email','password']

