from rest_framework import serializers
from user_sessions import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer to handle User instances"""
    class Meta:
        model = User
        fields = ['mobile_number','username']