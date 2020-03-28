from django.conf.urls import url
from django.urls import re_path
from . import views

urlpatterns = [
    url(r'^auth/$',
       views.SpotifyView.as_view(),
        name='authorized'),

    # url(r'^/auth/$',
    #     views.SpotifyView.as_view(),
    #     name='spotify')

]