from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend

from user_sessions.models import User

class CustomUserBackend(BaseBackend):
    def authenticate(self,request,username=None,password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(finin_id = user_id)
        except User.DoesNotExist:
            return None