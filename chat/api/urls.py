from django.urls import re_path,path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^makegroup/$',views.Make_Group,name="makegroup"),
    url(r'^groupinfo/$',views.Info_Groups,name='group_info'),
    url(r'^groupmember/$',views.Group_member,name='groupmember'),
    url(r'^showfriends/$',views.Show_friemd_to_add.as_view(),name='Show_friemd_to_add'),
    url(r'^addmember/$',views.Add_Members.as_view(),name='addmember'),
    url(r'^leavegroup/$',views.Leave_Group.as_view(),name='leavegroup'),
    url(r'^updatename/$',views.Change_Group_Name.as_view(),name='updatename'),

    url(r'^friendinfo/$',views.User_Friend_Info,name='User_Friend_Info'),
    path('', views.simple_chat, name='conv'),
    url(r'^inbox/$',views.all_inboxes,name='new-messages'),
    re_path('(?P<userparameter>\d{0,100}/$)', views.simple_chat, name='messages'),
    # path('inboxes', views.inboxes, name="inboxes")
]
