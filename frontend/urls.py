from django.urls import path
from .views import index, reset_password, register_page, login_page, forget_password, conversations
urlpatterns = [
    path('', index, name='index'),
    path('reset-password/', reset_password, name='password_reset'),
    path('forget-password/', forget_password, name='forget_password'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('conversations/', conversations, name='conversations'),
    path('conversations/create/', conversations, name='create_conversation'),
]