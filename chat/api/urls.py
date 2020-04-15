from django.urls import re_path,path

from . import views

urlpatterns = [
    path('', views.simple_chat, name='messsages'),
    re_path('(?P<userparameter>\d{0,100}/$)', views.simple_chat, name='messsages'),
    # path('inboxes', views.inboxes, name="inboxes")
]