from django.urls import path
from .views import UserRegsterationView, ListUsers

urlpatterns =[
    path('register/', UserRegsterationView.as_view(), name='register'),
    path('', ListUsers.as_view())
]