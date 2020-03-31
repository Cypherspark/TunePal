from django.conf.urls import url
from django.urls import re_path
from . import views

urlpatterns = [
    url(r'^auth/$',
       views.SpotifyView.as_view(),
        name='authorized'),
    url(r'^profile/(?P<pk>\d+)$',
            views. UserViewSet.as_view({'get': 'retrieve'}),
            name='profile'),
    url(r'^match/$',
       views.Match.as_view(),
        name='Matching'),
    # url(r'^/auth/$',
    #     views.SpotifyView.as_view(),
    #     name='spotify')


]
