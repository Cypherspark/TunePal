from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [

    url(r'^login/$',
        views.LoginView.as_view(),
        name='login'),

    url(r'^sign_up/$',
        views.SignupView.as_view(),
        name='register'),

    url(r'^get_location/$',
        views.UserLocationView.as_view(),
        name='location'),

    url(r'^get_user_info/$',
        views.UserInfoView.as_view(),
        name='user-info'),

    url(r'^logout/$',
        views.LogoutView.as_view(),
        name='logout'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
