from django.shortcuts import render
from .serializers import ConversationSerializer
from rest_framework import status
from .models import Conversation
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

# Create your views here.


class CreateConversation(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self,request,*args,**kwargs):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Converstaion Created Successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListConversations(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        return Response(ConversationSerializer(Conversation.objects.all(),many=True).data)



# class ReadConversation(APIView):

#     # permission_classes=[IsAuthenticated,]

#     def get(self,request,*args,**kwargs):
#         data = request.query_params.get('messages')
#         return Response({'Messages': data})