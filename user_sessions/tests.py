from django.test import TestCase, Client, SimpleTestCase
from user_sessions.models import User, UserSessions
from django.urls import reverse, resolve
from user_sessions import views
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.db import transaction

"""
Testing To Do:
            1)Integrity testing
            2)Urls testing
            3)Concurrent session testing using selenium web browser
            4)API freeze testing
"""

user_dict = {'username': "Lorem Ipsum", 'mobile_number': 123456}


class UserModelIntegrityTest(TestCase):
    """
    Tests to check the unique constrains of the User model.
    """

    def setUp(self):
        User.objects.create_user(
            username='abcabc', mobile_number='9999999999', password='9999999999')

    def test_to_check_unique_username(self):
        try:
            with transaction.atomic():
                _user = User.objects.create_user(
                    username='abcabc', mobile_number='8999999999', password='8999999999')
        except:
            pass
        count = User.objects.all().count()
        self.assertEqual(count, 1)

    def test_to_check_unique_mobile_numbers(self):
        try:
            with transaction.atomic():
                _user = User.objects.create_user(
                    username='abcabcd', mobile_number='9999999999', password='9999999999')
        except:
            pass
        count = User.objects.all().count()
        self.assertEqual(count, 1)

    def test_to_check_unique_mobile_number_and_username(self):
        try:
            with transaction.atomic():
                _user = User.objects.create_user(
                    username='abcabc', mobile_number='9999999999', password='9999999999')
        except:
            pass
        count = User.objects.all().count()
        self.assertEqual(count, 1)





class UserSessionUrlsTest(SimpleTestCase):
    """
    Test to resolve urls of user_sessions app
    """

    def test_signup_url(self):
        url = reverse('Sign_Up')
        self.assertEqual(resolve(url).func.__name__,
                         views.CreateUserView.as_view().__name__)

    def test_list_user_url(self):
        url = reverse('list')
        self.assertEqual(resolve(url).func.__name__,
                         views.ListUsersView.as_view().__name__)


