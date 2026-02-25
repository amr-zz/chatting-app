from django.urls import path
from .views import UserRegsterationView, ListUsers, register_page

urlpatterns =[
    path('register-page/', register_page),
    path('register/', UserRegsterationView.as_view(), name='register'),
    path('', ListUsers.as_view())
]