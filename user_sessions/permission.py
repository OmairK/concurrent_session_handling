from rest_framework import permissions
from user_sessions.models import UserSessions


class ValidSessionPermission(permissions.BasePermission):
    """
    Permission check for active session of the client.
    """
    message = "There is already session up and running, please logout and login again."
    def has_permission(self,request,view):
        print('HEEEEEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLOOOOOOOOOOOOOOoo')
        session = request.session.session_key
        try:
            user_session = UserSessions.objects.get(session=session)
        
            if user_session.is_active:
                return True
            return False
        except UserSessions.DoesNotExist:
            return False