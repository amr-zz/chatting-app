from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<int:conversation_id>/<str:conversation_name>/', consumers.ConversationConsumer.as_asgi()),
]