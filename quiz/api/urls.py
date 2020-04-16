from django.conf.urls import url
from django.urls import re_path
from . import views

urlpatterns = [

    url(r'^question/$',
       views.question.as_view(),
        name='question'),
    url(r'^Imagequiz/$',
       views.Imagequiz.as_view(),
        name='Imagequiz'),
    url(r'^passagequiz/$',
       views.passagequiz.as_view(),
        name='passagequiz'),
    url(r'^checkimageanswer/$',
       views.checkimageanswer.as_view(),
        name='checkimageanswer'),
    url(r'^checkpssageanswer/$',
       views.checkpssageanswer.as_view(),
        name='checkpssageanswer'),
    url(r'^score/$',
       views.getscore.as_view(),
        name='score'),



]
