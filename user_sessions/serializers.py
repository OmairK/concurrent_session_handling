from rest_framework import serializers

from user_sessions.models import User,UserSessions


class UserSessionKeySerializer(serializers.ModelSerializer):
    """ Serialializer to handle the user_session instances"""
    
    class Meta:
        model = UserSessions
        # fields = ('sessions','is_active')
        fields = '__all__'

        

class UserAndUserSessionSerializer(serializers.ModelSerializer):
    """ Serializer to handle the user and nested user_session details"""
    session = UserSessionKeySerializer(many=True)
    class Meta:
        model = User
        fields = ('mobile_number','username','session')
        depth = 1

class UserSerializer(serializers.Serializer):
    """Serializer to handle User instances"""
    username = serializers.CharField(max_length=100)
    mobile_number = serializers.IntegerField()

    def create(self, validated_data):
        print(f'{request.user} is the wayyyyyyy')
        return User.objects.create_user(username=validated_data['username'], 
                                    mobile_number=validated_data['mobile_number'],
                                    password=validated_data['mobile_number'])

