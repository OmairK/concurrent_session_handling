from rest_framework import serializers
from user_sessions.models import User


class UserSerializer(serializers.Serializer):
    """Serializer to handle User instances"""
    username = serializers.CharField(max_length=100)
    mobile_number = serializers.IntegerField()

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'], 
                                    mobile_number=validated_data['mobile_number'],
                                    password=validated_data['mobile_number'])
