from django.conf.urls import url
from django.urls import re_path
from . import views

urlpatterns = [

    url(r'^question/$',
       views.question.as_view(),
        name='question'),
    url(r'^quiz/$',
       views.quiz.as_view(),
        name='quiz'),
        url(r'^checkanswer/$',
       views.checkanswer.as_view(),
        name='checkanswer'),

    url(r'^score/$',
       views.getscore.as_view(),
        name='score'),



]
