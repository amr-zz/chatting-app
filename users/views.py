from django.shortcuts import render
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import MyUser
from rest_framework.views import APIView

# Create your views here.

class UserRegsterationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh),
                             'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def register_page(request):
    return render(request,"register.html")

class ListUsers(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        return Response(UserSerializer(MyUser.objects.all(),many=True).data)
