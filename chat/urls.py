from django.urls import path
from .views import (CreateConversation,
                    ListConversations,
                    DetailConversation,
                    DisplayConversationMessages,
                    UpdateConversation,
                    DeleteConversation,
                    SendMessage,
                    UpdateMessage,
                    DeleteMessage,
                    DiscoverConversations,
                    JoinConversation,)


urlpatterns = [
    path('', ListConversations.as_view(), name='list-convos'),
    path('discover/', DiscoverConversations.as_view(), name='discover-convos'),
    path('<int:pk>/', DetailConversation.as_view()),
    path('join/<int:pk>/', JoinConversation.as_view()),
    path('update/<int:pk>/', UpdateConversation.as_view()),
    path('delete/<int:pk>/', DeleteConversation.as_view()),
    path('messages/<int:pk>/',DisplayConversationMessages.as_view()),
    path('create/', CreateConversation.as_view()),
    path('messages/create/<int:pk>/', SendMessage.as_view()),
    path('messages/update/<int:pk>/', UpdateMessage.as_view()),
    path('messages/delete/<int:pk>/', DeleteMessage.as_view()),
]