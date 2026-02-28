from django.shortcuts import redirect, render, get_object_or_404
from chat.models import Conversation
import json
from chat.serializers import ConversationSerializer

# Create your views here.

def index(request):
    return render(request, 'frontend/index.html')


def login_page(request):
    return render(request, 'frontend/login.html')

def forget_password(request):
    return render(request, 'frontend/forget_password.html')

def reset_password(request):
    return render(request, 'frontend/reset_password.html')

def register_page(request):
    return render(request, 'frontend/register.html')

def conversations(request):
    return render(request, 'frontend/conversations.html')

def create_conversation(request):
    return render(request, 'frontend/create_edit_group.html', {'is_edit': False, 'group': None})

def edit_conversation(request, pk=None):
    conversation = ConversationSerializer(Conversation.objects.filter(pk=pk).first())
    if conversation:
        return render(request, 'frontend/create_edit_group.html', {'is_edit': True, 'group':conversation.data})
    else:
        return redirect('/conversations/create/')
    
def discover_conversations(request):
    return render(request, 'frontend/discover_groups.html')


def conversation_chat(request, conversation_id=None):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    return render(request, 'frontend/chatting.html', {
        'conversation': conversation
    })