from django.contrib.auth import user_logged_in, user_logged_out
from user_sessions.models import UserSessions
from django.dispatch import reciever


def get_client_ip(request):
    """
    Function to resolve the IP address of the user.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@reciever(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Signal to deactivate the older of the concurrent sessions of the user.
    """
    print('HHELLLLLLLLLLLLLLLLLLLLLLLLLLL')
    try:
        _session = UserSessions.objects.get(user=user, is_active=True)
        _session.is_active = False
        _session.save()
    except UserSessions.DoesNotExist:

    session = UserSessions.objects.create(
        user=user, session=request.session.session_key,
        user_ip=get_client_ip(request), is_active=True)
    session.save()


# user_logged_in.connect(user_logged_in_handler)

@reciever(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    """
    Signal to deactivate the session when the user logs-out
    """
    print('BYEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEe')
    _session = UserSessions.objects.get(
        user=user, session=request.session.session_key)
    _session.is_active = False
    _session.save()


# user_logged_out.connect(user_logged_out_handler)
