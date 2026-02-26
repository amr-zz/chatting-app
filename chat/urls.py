from django.urls import path
from .views import CreateConversation,ListConversations


urlpatterns = [
    path('', ListConversations.as_view(), name='list-convos'),
    path('create/', CreateConversation.as_view())
]