from rest_framework.response import Response
from rest_framework.decorators import api_view, schema, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from chat.models import Message, Conversation
from chat.api.serializers import *
from rest_framework.permissions import IsAuthenticated

from account.models import CustomUser,Friend
from django.shortcuts import get_object_or_404


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
        serializer_class = FriendInfoSerializer(friend.users,context={'request': request},many = True)
        return Response(serializer_class.data)
    except Exception as e:
         serializer_class = FriendInfoSerializer(friend.users,context={'request': request},many = True)
         return Response([])
