from django.conf.urls import url


from . import views

urlpatterns = [

    url(r'^login/$',
        views.LoginView.as_view(),
        name='login'),

    url(r'^sign_up/$',
        views.SignupView.as_view(),
        name='register'),
    url(r'^profile$',
            views. UserProfile.as_view({'get': 'retrieve'}),
            name='profile'),
    url(r'^update$',
            views. UpdateUser.as_view(),
            name='update'),
]
