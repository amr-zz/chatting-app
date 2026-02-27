from django.db import models
from users.models import MyUser
from datetime import datetime
# Create your models here.





class Conversation(models.Model):
    conversation_name = models.CharField(max_length=256)
    conversation_description = models.TextField()
    conversation_created_by = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING,related_name='created_by')
    members = models.ManyToManyField(MyUser,related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,related_name='messages')
    message_content = models.CharField(max_length=1024)
    message_sender = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message_sent_at = models.DateTimeField(auto_now_add=True)