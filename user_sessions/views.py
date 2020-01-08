from django.shortcuts import render
from rest_framework import generics
from user_sessions.serializers import UserSerializer
from user_sessions.models import User
from rest_framework import permissions

class CreateUserView(generics.ListCreateAPIView):
    """
    API View to list and create users. 
    """
    permission_classes=[permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()
