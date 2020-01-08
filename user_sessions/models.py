from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as _UserManager
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.conf import settings
from django.contrib.sessions.models import Session

import uuid


class UserManager(_UserManager):
    def create_user(self, username, mobile_number, password=None):
        """
        Creates and saves a user with the provided 
        username and mobile_number
        """
        
        if not username or not password:
            raise ValueError('Users must enter username and password')

        user = self.model(username=username, mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the provided username,mobile_number
        """
        
        user = self.create_user(
            username=username,
            password=password,
            mobile_number=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractBaseUser
    """
    finin_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    mobile_number = models.BigIntegerField(verbose_name='mobile number')
    username = models.CharField(max_length=100, unique=True)
    # password = models.CharField(max_length=20, verbose_name='password')
    is_staff = models.BooleanField(verbose_name='is staff', default=False)
    is_superuser = models.BooleanField(
        verbose_name='is superuser', default=False)
    is_active = models.BooleanField(verbose_name='is active', default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    def get_short_name(self):
        return self.username    
    
    def get_long_name(self):
        return self.username

    objects = UserManager()


class UserSessions(models.Model):
    """
    Model to handle the relation between the user and its session.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    session = models.OneToOneField(Session, on_delete=models.SET_NULL,null=True)
    user_ip = models.GenericIPAddressField(
        protocol='both', unpack_ipv4=False, blank=True, null=True,)
    date_time_of_session_start = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(
        default=True, verbose_name='session active')

from django.contrib.auth import user_logged_in, user_logged_out
from user_sessions.models import UserSessions
from django.dispatch import receiver


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

@receiver(user_logged_in)
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
        pass
    print(request.session.values())
    session = UserSessions.objects.create(
        user=user, session=request.session,
        user_ip=get_client_ip(request), is_active=True)
    session.save()


# user_logged_in.connect(user_logged_in_handler)

@receiver(user_logged_out)
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
