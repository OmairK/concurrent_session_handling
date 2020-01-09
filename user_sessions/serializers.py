from rest_framework import serializers
from user_sessions.models import User, UserSessions
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError


class VerboseUserSession(serializers.ModelSerializer):
    """Verbose session details serializer"""
    class Meta:
        model = UserSessions
        fields = ('session', 'user_ip', 'user_agent','is_active')


class UserSessionKeySerializer(serializers.ModelSerializer):
    """ Serialializer to handle the user_session instances"""
    class Meta:
        model = UserSessions
        fields = ('session', 'is_active',)


class UserAndUserSessionSerializer(serializers.ModelSerializer):
    """ Serializer to handle the user and nested user_session details"""
    sessions = UserSessionKeySerializer(many=True,)

    class Meta:
        model = User
        fields = ('mobile_number', 'username', 'active_session', 'sessions',)
        depth = 1


class UserAndVerboseUserSessionSerializer(serializers.ModelSerializer):
    """Serializer to handle the user and nested verbose user session details"""
    sessions = VerboseUserSession(many=True)

    class Meta:
        model = User
        fields = ('mobile_number', 'username', 'active_session', 'sessions',)


class UserSerializer(serializers.Serializer):
    """Serializer to handle User instances"""
    username = serializers.CharField(max_length=100)
    mobile_number = serializers.IntegerField()

    def create(self, validated_data):
        try:
            return User.objects.create_user(username=validated_data['username'],
                                            mobile_number=validated_data['mobile_number'],
                                            password=validated_data['mobile_number'])
        except IntegrityError:
            raise serializers.ValidationError('This username or mobile number is already registered')

