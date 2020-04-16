from rest_framework.response import Response
from rest_framework.decorators import api_view, schema, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from chat.models import Message, Conversation
from chat.api.serializers import *
from rest_framework.permissions import IsAuthenticated


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




# def inboxes(request):
#     users_list = Users.objects.all()
#     for u in users_list:
#         u.recieved_messages = 0
#         for c in u.conversations_set.all():
#             u.recieved_messages += len(Messages.objects.filter(Q(conversation_id = c)).filter(~Q(sender_id=u)))

#     return render(
#                   request,
#                   "inboxes.html",{
#                     "users_list":users_list,  
#                   }
#             )