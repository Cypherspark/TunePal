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
        name='get-token-spotify'),
    url(r'^score/$',
            views. UserUpdateScore.as_view(),
            name='scoreupdate'),
    url(r'^topsong/$',
            views. User_Top_Music.as_view(),
            name='topsong'),
    url(r'^question/$',
       views.question.as_view(),
        name='question'),

    url(r'^quiz/$',
       views.privatequiz.as_view(),
        name='quiz'),
    url(r'^check/$',
       views.checkanswer.as_view(),
        name='checkanswer'),
    url(r'^publicquiz/$',
       views.publicquiz.as_view(),
        name='publicquiz'),
    # url(r'^Top/$',
    #     views.Top_Artist.as_view(),
    #     name='TopArtist')

]
