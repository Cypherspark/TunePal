from django.conf.urls import url
from django.urls import re_path
from . import views

urlpatterns = [
    url(r'^auth/$',
       views.SpotifyView.as_view(),
        name='make-auth-uri'),

    url(r'^get_url/$',
        views.SpotifyGetTokenView.as_view(),
        name='get-token-spotify')

]