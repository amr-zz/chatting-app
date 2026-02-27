from django.shortcuts import render

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
    return render(request, 'frontend/create_edit_group.html')