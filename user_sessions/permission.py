from rest_framework import permissions
from user_sessions.models import UserSessions


class ValidSessionPermission(permissions.BasePermission):
    """
    Permission checks if the client's current session is active .
    """
    message = "There is already session up and running, please logout and login again."
    def has_permission(self,request,view):
      
        session = request.session.session_key
        try:
            user_session = UserSessions.objects.get(session=session)
        
            if user_session.is_active:
                return True
            return False
        except UserSessions.DoesNotExist:
            return False