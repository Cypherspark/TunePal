from django.conf.urls import url
from django.urls import re_path
from . import views

urlpatterns = [
    url(r'^auth/$',
       views.SpotifyView.as_view(),
        name='make-auth-uri'),

    url(r'^get_url/$',
        views.SpotifyGetTokenView.as_view(),
        name='get-token-spotify'),

    # url(r'^savesong/$',
    #         views.User_Top_Music.as_view(),
    #         name='topsong'),
    url(r'^topsong/$',
            views.User_Top_Music.as_view(),
            name='topsong'),
    url(r'^topartist/$',
            views. User_Top_Artist.as_view(),
            name='topartist'),

    url(r'^suggestions/$',
        views.SuggestUserView.as_view(),
        name='user-suggestions'),

    url(r'^friend_list/$',
            views.Friend_Request_View.as_view(),
            name='Friend_Request_View'),

    url(r'^friend_request/$',
            views.Friend_Request.as_view(),
            name='Friend_Request'),

    url(r'^response/$',
            views.Add_Or_Reject_Friends.as_view(),
            name='add-or-remove-friend'),

]
