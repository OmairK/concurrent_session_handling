from django.shortcuts import render
from rest_framework import generics
from user_sessions.serializers import (
    UserSerializer, UserAndUserSessionSerializer, 
    UserSessionKeySerializer, UserAndVerboseUserSessionSerializer)
from user_sessions.models import User, UserSessions
from rest_framework import permissions
from user_sessions.permission import ValidSessionPermission
from django.shortcuts import get_object_or_404


class CreateUserView(generics.ListCreateAPIView):
    """
    API View to list and create users. 
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ListUsersView(generics.ListAPIView):
    """
    API View to test the valid session 
    """
    permission_class = (ValidSessionPermission,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ListClientSession(generics.RetrieveAPIView):
    """
    API view to retrieve details of a client's sessions
    """
    serializer_class = UserAndUserSessionSerializer
    queryset = User.objects.all()
    lookup_field = 'mobile_number'

    def get_object(self):
        mobile_number = self.kwargs['mobile_number']
        return get_object_or_404(User, mobile_number=mobile_number)


class ListVerboseClientSessions(generics.RetrieveAPIView):
    """
    API view to retrieve verbose details of a client's sessions
    """
    serializer_class = UserAndVerboseUserSessionSerializer
    queryset = UserSessions.objects.all()
    lookup_field = 'mobile_number'

    def get_object(self):
        mobile_number = self.kwargs['mobile_number']
        return get_object_or_404(User, mobile_number=mobile_number)
