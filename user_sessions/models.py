from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as _UserManager
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.conf import settings
from django.contrib.sessions.models import Session

import uuid


class UserManager(_UserManager):
    def create_user(self, username, mobile_number):
        """
        Creates and saves a user with the provided 
        username and mobile_number
        """
        if not username or not mobile_number:
            raise ValueError('Users must enter username and mobile number')

        user = self.model(username=username, mobile_number=mobile_number)
        user.set_password(mobile_number)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, mobile_number):
        """
        Creates and saves a superuser with the provided username,mobile_number
        """
        user = self.create_user(
            username=username,
            password=mobile_number,
            mobile_number=mobile_number,
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
    password = models.CharField(max_length=20, verbose_name='password')
    is_staff = models.BooleanField(verbose_name='is staff', default=False)
    is_superuser = models.BooleanField(
        verbose_name='is superuser', default=False)
    is_active = models.BooleanField(verbose_name='is active', default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserSessions(models.Model):
    """
    Model to handle the relation between the user and its session.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,null=True)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField(
        protocol='both', unpack_ipv4=False, blank=True, null=True,)
    date_time_of_session_start = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(
        default=True, verbose_name='session active')
