from rest_framework.response import Response
from rest_framework.decorators import api_view, schema, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from chat.models import Message, Conversation
from chat.api.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from account.models import CustomUser,Music,Friend
from django.http import HttpResponse
from chat.models import Group,Admin,GroupMessage
from django.shortcuts import render
from chat.consumers import ChatConsumer


@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['GET', 'POST'])
def simple_chat(request, userparameter=None):


    if request.method == 'GET':

        if  userparameter == None:
                c = Conversation.objects.filter(members__id = request.user.id)
                conversation_list = ConversationSerializer(c, many=True, context={'request': request})
                print("here")

                return Response(
                {
                    "conversations": conversation_list.data
                }
            )

        else:
            try:
                userparameter = '/'.join(e for e in userparameter if e.isalnum())
                selected_conv = Conversation.objects.filter(id=int(userparameter))[0]
                # users = selected_conv.members.all()
                M = Message.objects.filter(conversation_id = int(userparameter)).all()
                message_list = MessageSerializer(M, many=True, context={'request': request})
                for message in message_list:
                    if message.sender_id.id != request.user.id:
                        message.is_seen = True
            except :
                M = []
                users = []

            return Response(
                {
                    # "users": user_list,
                    "messages": message_list.data,
                }
            )



    elif request.method == "POST":
        userparameter = '/'.join(e for e in userparameter if e.isalnum())
        # .get(id = room_name)
        # users_len = len(users)
        c = Conversation.objects.filter(id=int(userparameter))[0]
        serializer = MessageSerializer(data=request.data, context={'request': request, 'coversation_id': c})
        if serializer.is_valid():
            m = serializer.save()
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

        # users = c.members.all()
        # user_list = ProfileSerilizer(users, many=True)


        M = Message.objects.filter(
            conversation_id=int(userparameter)
        )
        message_list = MessageSerializer(M, many=True ,context={'request': request})




        return Response(
            {
                # "users": user_list,
                "messages": message_list.data,
            }
        )


@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['GET'])
def all_inboxes(request):
    if request.method == 'GET':
        user = request.user
        recieved_messages = 0
        for c in u.conversations_set.all():
            recieved_messages += len(Messages.objects.filter(Q(conversation_id = c)).filter(~Q(sender_id=u)).filter(Q(is_seen=False)))

        return Response(
                    {"new_messages":recieved_messages}
                )
# @permission_classes([IsAuthenticated])
# @csrf_exempt
# @api_view(['GET'])
from django.contrib.auth.models import Permission

# def room(request, room_name):
#     user = get_object_or_404(CustomUser,id = 3)
#     # user1 = get_object_or_404(CustomUser,id = 2)
#     # Friend.make_friend(user,user1)
#     # friend = Friend.objects.get(current_user = user)
#     # friend.users.add(user1)
#     # print(friend.users.all())
#     # for x in friend.users.all():
#     #     print(x.username)
#
#     group = Conversation.objects.filter(members__id = user.id)
#       # serializers_class = GroupSerializer(group,many =True)
#     flag = False
#     for i in range(group.count()):
#         print(group[i].name)
#         if room_name == group[i].name:
#             print(room_name)
#             ChatConsumer.sender_id = user
#             ChatConsumer.conversation_id = group[i]
#             # ChatConsumer.userparameter = userparameter
#             return render(request, 'friend.html', {
#             'room_name': room_name
#                 })
#             flag = True
#             break
#     print(flag)
#     if flag == False :
#         return HttpResponse("you dont have a group with this name")
#     else:
#         return HttpResponse("done")
# # def makegroup(request,room_name):
# #     user = get_object_or_404(CustomUser,id = request.user.id)
# #     admin = Admin.objects.create()
# #     admin.admin.add(user)
# #     g = Group.objects.create(group_name =room_name)
# #     g.admin.add(admin)
# #     g.members.add(user)
# #     # print(g)
# #     return HttpResponse("done")
def add_member(request,room_name,username):
    group = Conversation.objects.get(name = room_name)
    admin = group.admin.all()
    member = CustomUser.objects.get(username = username)
    SendEmail(request,str(member.email),"friend.html",member.username,admin.username)
    if request.user in admin :
        group.members.add(member)
        group.save()

def remove_member(request,room_name,username):
    group = Conversation.objects.get(name = room_name)
    admin = group.admin.all()
    member = CustomUser.objects.get(username = username)
    if request.user in admin :
        group.members.remove(member)
        group.save()

def add_Admin (request,member_username,conv_name):
    user  = get_object_or_404(CustomUser,id = request.user.id )
    member = get_object_or_404(CustomUser,username = member_username )

    group = Conversation.objects.get(name = conv_name)
    admin = group.admin.all()
    if user in admin:
        if member in group.members.all() :
            group.admin.add(member)
            group.save()
            return HttpResponse("member added to admin ")
        else:
            return HttpResponse("this user not in members")

    return HttpResponse(admin)
def remove_Admin (request,member_username,conv_name):
    user  = get_object_or_404(CustomUser,id = request.user.id )
    member = get_object_or_404(CustomUser,username = member_username )

    group = Conversation.objects.get(name = conv_name)
    admin = group.admin.all()
    if user in admin:
        if member in group.members.all() :
            group.admin.remove(member)
            group.save()
            return HttpResponse("member removed to admin ")
        else:
            return HttpResponse("this user not in members")

    return HttpResponse(admin)
def online_user(request,conv_name):
    group = Conversation.objects.get(name = conv_name)
    online_list = []
    for user in group.members.all():
        if user.status == "online":
            online_list.append(user)
    return Response(online_list)
def SendEmail(request,recepient,html,usernameofn_f,usernameofowner):
    if request.method == 'GET':
        subject = 'Welcome to TunePal'
        html_message = render_to_string(html,{'usernameofn_f':usernameofn_f,'usernameofowner' :usernameofowner})
        message = strip_tags(html_message)
        message1 =EmailMultiAlternatives(subject,
            message, EMAIL_HOST_USER, [recepient])
        message1.attach_alternative(html_message, 'text/html')
        message1.send()
        return HttpResponse('done')
    else:
        return HttpResponse('fialed')
def left_group(request,conv_name,username):
    member = CustomUser.objects.get(user = request.user)
    group = Conversation.objects.get(name = conv_name)
    group.members.remove(member)
    group.save()
    return Response("done")
def edit_message(request,old_message,conv_name,new_message):
    group = Conversation.objects.get(name = conv_name)
    message = Message.objects.get(conversation_id = group,text = old_message)
    message.text = new_message
    message.save()
    return Response("done")
def set_pin_message(request,message,conv_name):
    group = Conversation.objects.get(name = conv_name)
    group.pin_message = message1
    group.save()
    return Response(group.pin_message)

def pin_message(request,conv_name):
    group = Conversation.objects.get(name = conv_name)
    return Response(group.pin_message)




# @swagger_auto_schema(tags=['Match'],request.usersponses={200: openapi.Response('ok')})
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def get(self, request):
#     username  = request.GET['username']
#     n_f = get_object_or_404(User, username=username)
#     owner = request.user
#     FR = FriendshipRequest(from_user=owner, to_user=n_f)
#     FR.save()
#     SendEmail(request,str(n_f.email),"friend.html",n_f.username,owner.username)
#     return Response(status=status.HTTP_200_OK)
