from django.urls import re_path,path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lastimage/$',
        views.LastAvatar.as_view(),
        name='lastimage'),
    path('', views.simple_chat, name='conv'),
    url(r'^inbox/$',views.all_inboxes,name='new-messages'),
    re_path('(?P<userparameter>\d{0,100}/$)', views.simple_chat, name='messages'),

    # path('inboxes', views.inboxes, name="inboxes")
]
