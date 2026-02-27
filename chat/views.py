from django.shortcuts import render
import json
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import status
from .models import Conversation, Message
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

# Create your views here.


class CreateConversation(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self,request,*args,**kwargs):
        serializer = ConversationSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Converstaion Created Successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListConversations(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(ConversationSerializer(Conversation.objects.filter(members=request.user),many=True).data)
    
class DetailConversation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        qs = Conversation.objects.filter(pk=pk, members=request.user)
        if not qs.exists():
            return Response({"error": f"Conversation with id {pk} not found or you are not a member."},status=status.HTTP_404_NOT_FOUND)
        serializer = ConversationSerializer(qs[0])
        return Response(serializer.data)
    
class DisplayConversationMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk=None, format=None):

        qs = Conversation.objects.filter(pk=pk, members=request.user)
        if not qs.exists():
            return Response({"error": f"Conversation with id {pk} not found or you are not a member."},status=status.HTTP_404_NOT_FOUND)
        serializer = ConversationSerializer(qs[0])
        return Response(serializer.data['messages'])

class UpdateConversation(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def patch(self, request, pk=None, format=None):

        try:
            conversation = Conversation.objects.get(pk=pk, members=request.user)
        except Conversation.DoesNotExist:
            return Response({"message": f"Conversation with id {pk} not found or you are not a member."}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, conversation)
        serializer = ConversationSerializer(conversation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Conversation updated successfully!"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class DeleteConversation(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, pk=None, format=None):
        try:
            conversation = Conversation.objects.get(pk=pk, members=request.user)
        except Conversation.DoesNotExist:
            return Response({"message": f"Conversation with id {pk} not found or you are not a member."}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, conversation)
        conversation.delete()
        return Response({"message": "Conversation deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

class SendMessage(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None, format=None):
        try:
            conversation = Conversation.objects.get(pk=pk, members=request.user)
        except Conversation.DoesNotExist:
            return Response({"message": f"Conversation with id {pk} not found or you are not a member."}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation=conversation, message_sender=request.user)
            return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateMessage(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def patch(self, request, pk=None, format=None):
        try:
            message = Message.objects.get(pk=pk, message_sender=request.user)
        except Message.DoesNotExist:
            return Response({"message": f"Message with id {pk} not found or you are not the sender."}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, message)
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message updated successfully!"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteMessage(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, pk=None, format=None):
        try:
            message = Message.objects.get(pk=pk, message_sender=request.user)
        except Message.DoesNotExist:
            return Response({"message": f"Message with id {pk} not found or you are not the sender."}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, message)
        try: 
            message.delete()
        except Exception as e:
            return Response({"message": f"An error occurred while deleting the message: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Message deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        