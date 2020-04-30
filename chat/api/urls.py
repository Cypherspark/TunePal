from django.urls import re_path,path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.simple_chat, name='messsages'),
    re_path('(?P<userparameter>\d{0,100}/$)', views.simple_chat, name='messsages'),
    url(r'^inbox/$',views.all_inboxes,name='new-messages'),
    # path('inboxes', views.inboxes, name="inboxes")
]