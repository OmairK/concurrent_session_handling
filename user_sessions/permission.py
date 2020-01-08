# from rest_framework import permissions
# from user_sessions.models import UserSessions


# class ValidSessionPermission(permissions.BasePermissions):
#     """
#     Permission check for concurrent sessions
#     """
#     def has_permission(self,request,view):
#         session = request.session
#         user_session = UserSessions.objects.get(session=session)
#         if user_session.is_active:
#             return True
#         return False