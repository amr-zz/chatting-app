from django.urls import path
from .views import conversation_chat, index, reset_password, register_page, login_page, forget_password, conversations, create_conversation,edit_conversation, discover_conversations
urlpatterns = [
    path('', index, name='index'),
    path('chat/<int:conversation_id>/', conversation_chat, name='conversation_chat'),
    path('reset-password/', reset_password, name='password_reset'),
    path('forget-password/', forget_password, name='forget_password'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('conversations/', conversations, name='conversations'),
    path('conversations/create/', create_conversation, name='create_conversation'),
    path('conversations/edit/<int:pk>/', edit_conversation, name='edit_conversation'),
    path('discover_conversations/', discover_conversations, name='view_conversation'),
    path('conversations/<int:conversation_id>/', conversation_chat, name='chat'),
]