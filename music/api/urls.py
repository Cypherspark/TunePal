from django.conf.urls import url
from django.urls import re_path
from . import views

urlpatterns = [
    url(r'^auth/$',
       views.SpotifyView.as_view(),
        name='make-auth-uri'),

    url(r'^friends/$',
       views.Find_friends.as_view(),
        name='Find_friends'),
    url(r'^match/$',
       views.Match.as_view(),
        name='Matching'),
    # url(r'^/auth/$',
    #     views.SpotifyView.as_view(),
    #     name='spotify')
    url(r'^get_url/$',
        views.SpotifyGetTokenView.as_view(),
        name='get-token-spotify')


]
