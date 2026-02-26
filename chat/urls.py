from django.urls import path
from .views import (CreateConversation,
                    ListConversations,
                    DetailConversation,
                    DisplayConversationMessages,
                    UpdateConversation,
                    DeleteConversation)


urlpatterns = [
    path('', ListConversations.as_view(), name='list-convos'),
    path('<int:pk>/', DetailConversation.as_view()),
    path('update/<int:pk>/', UpdateConversation.as_view()),
    path('delete/<int:pk>/', DeleteConversation.as_view()),
    path('messages/<int:pk>/',DisplayConversationMessages.as_view()),
    path('create/', CreateConversation.as_view())
]