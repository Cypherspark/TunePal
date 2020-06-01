from rest_framework.response import Response
from rest_framework.decorators import api_view, schema, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from chat.models import Message, Conversation
from chat.api.serializers import *
from rest_framework.permissions import IsAuthenticated

from account.models import CustomUser,Friend
from django.shortcuts import get_object_or_404

import ast

from rest_framework.views import APIView


@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['GET', 'POST'])
def simple_chat(request, userparameter=None):


    if request.method == 'GET':

        if  userparameter == None:
                c = Conversation.objects.filter(members__id = request.user.id)
                conversation_list = ConversationSerializer(c, many=True, context={'request': request})

                return Response(
                {
                    "conversations": conversation_list.data
                }
            )

        else:
            print(userparameter)
            try:
                userparameter = userparameter.strip("/")
                selected_conv = Conversation.objects.filter(id=int(userparameter))[0]
                # users = selected_conv.members.all()
                M = Message.objects.filter(conversation_id = int(userparameter)).order_by('date')
                message_list = MessageSerializer(M, many=True, context={'request': request})
                for message in M:
                    if message.sender_id.id != request.user.id:
                        message.is_seen = True
                        message.save()

                return Response(
                {
                    # "users": user_list,
                    "messages": message_list.data,
                }
            )
            except Exception as e:
                print(str(e))
                message_list = []
                users = []

                return Response(
                    {
                        # "users": user_list,
                        "messages": message_list
                    }
                )



    elif request.method == "POST":
        userparameter = '/'.join(e for e in userparameter if e.isalnum())

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
        conversations_set =  Conversation.objects.filter(members__id = request.user.id)
        recieved_messages = 0
        for c in conversations_set:
            kos = list(Message.objects.filter(Q(conversation_id = c)).filter(is_seen=False).filter(~Q(sender_id__id=user.id)))
            recieved_messages += len(kos)
            print(kos)
        return Response(
                    {"new_messages":recieved_messages}
                )

@api_view(['GET'])
def User_Friend_Info(request):
    user = get_object_or_404(CustomUser, id = request.user.id)
    try:
        friend = Friend.objects.get(current_user = user)
        serializer_class = FriendInfoSerializer(friend.users.all(),context={'request': request},many = True)
        return Response(serializer_class.data)
    except Exception as e:
         return Response([])
@api_view(['POST'])
def Make_Group(request):
    l =  str(request.data["name"]).split(",")
    group = Conversation.objects.create(name = l[0])
    group.members.add(request.user)
    group.is_group = True
    l.remove(group.name)
    for x in l :
        member = CustomUser.objects.get(username = x)
        group.members.add(member)
        group.save()
    return Response("Done")
@api_view(['GET'])
def Info_Groups(request):
    c = Conversation.objects.filter(members__id = request.user.id,is_group = True)
    conversation_list = ConversationSerializer(c, many=True, context={'request': request})

    return Response({"conversations": conversation_list.data})

@api_view(['POST'])
def Group_member(request):
    c = Conversation.objects.get(id = request.data["id"])
    users = c.members
    conversation_list = Memberserializers(users,many = True,context={'request': request})
    return Response({"conversations": conversation_list.data})

class Show_friemd_to_add(APIView):
    def post(self,request):
        print(request.data)
        user = get_object_or_404(CustomUser, id = request.user.id)
        group = Conversation.objects.get(id = request.data["id"])
        try:
            friend = Friend.objects.get(current_user = user)
            print(friend.users.all())
            serializer_class = FriendInfoSerializer(friend.users.all(),context={'request': request},many = True)
            l = []
            for x in friend.users.all():

                if x not in group.members.all():
                    m = FriendInfoSerializer(x,context={'request': request})
                    l.append(m.data)

                    # l.append(x)

            return Response(l)
        except Exception as e:
             serializer_class = FriendInfoSerializer(friend.users,context={'request': request},many = True)
             return Response(["fcdx"])
class Add_Members(APIView):
    def post(self,request):
        l =  str(request.data["addedusers"]).split(",")
        group = Conversation.objects.get(id = request.data["id"])
        for x in l :
            member = CustomUser.objects.get(username = x)
            group.members.add(member)
            group.save()
        return Response("Users added")

class Leave_Group(APIView):
    def post(self,request):
        group = Conversation.objects.get(id = request.data["id"])
        member = CustomUser.objects.get(id = request.user.id)
        group.members.remove(member)
        group.save()

        return Response("User lefted")
