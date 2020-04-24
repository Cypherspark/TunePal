import hashlib, binascii, os
from music.models import Artist,Music
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import datetime



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
    artists = models.ManyToManyField(Artist, default=None,blank=True)
    tracks = models.ManyToManyField(Music,blank=True)
    status = models.CharField(blank = True,max_length = 10)
    top_artist = models.CharField(blank = True,max_length = 100)
    score = models.CharField(blank = True,max_length = 100000000, default = '0')


    location = models.OneToOneField(UserLocation,
                    blank=True,
                    null=True,
                    verbose_name=_("location"),
                    on_delete=models.CASCADE
                    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['gender', 'email','password']







class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name="invitations_from",on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name="invitations_to",on_delete=models.CASCADE)
    message = models.CharField(max_length=200, blank=True)
    # created = models.DateTimeField(default=datetime.datetime.now,
                                #    editable=False)
    accepted = models.BooleanField(default=False)

    @classmethod
    def accept(cls, owner, n_f):
        friendshipRequest, created = cls.objects.get_or_create(
            from_user = n_f,
            to_user = owner
        )
        Friend.make_friend(n_f, owner)
        Suggest.remove_suggest(n_f, owner)
        friendshipRequest.accepted = True
        friendshipRequest.save()

    @classmethod
    def decline(cls, owner, n_f):
        friendshipRequest, created = cls.objects.get_or_create(
            from_user = n_f,
            to_user = owner
        )
        Suggest.remove_suggest(n_f, owner)
        friendshipRequest.delete()

    # def cancel(self):
    #     signals.friendship_cancelled.send(sender=self)
    #     self.delete()



class Friend(models.Model):
    users = models.ManyToManyField(CustomUser,related_name="friends",blank=True)
    current_user = models.ForeignKey(CustomUser, related_name="owner", null=True, on_delete=models.CASCADE)
   
    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)
        friend, created = cls.objects.get_or_create(
            current_user = new_friend
        )
        friend.users.add(current_user)


    @classmethod
    def remove_friend(cls, current_user, new_friend):
        suggest, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend)


    def __str__(self):
        return str(self.current_user)



class Suggest(models.Model):
    s_users = models.ManyToManyField(CustomUser,related_name="s_users",blank=True)
    s_current_user = models.ForeignKey(CustomUser, related_name="s_owner", null=True, on_delete=models.SET_NULL)

    @classmethod
    def remove_suggest(cls, current_user, new_friend):
        suggest, created = cls.objects.get_or_create(
            s_current_user = current_user
        )
        suggest.s_users.remove(new_friend)

    def __str__(self):
        return str(self.s_current_user)
