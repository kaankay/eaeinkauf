from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Group, AnonymousUser
from django.urls import reverse
from seaeinkauf.views import group_check


class TestUserLoginLogout(TestCase):
    def setUp(self):
        self.client = Client()

        self.username = 'test_user'
        self.password = 'test_password'
        
        self.test_user = User.objects.create_user(self.username, 'tests@email.com', self.password)
        Group.objects.get_or_create(name='Weaeinkauf')
        weaeinkauf_group = Group.objects.get(name='Weaeinkauf')
        self.test_user .groups.add(weaeinkauf_group)
        return super().setUp()
    
    def test_group_check(self):
        user_has_group = group_check(self.test_user)
        self.assertTrue(user_has_group)
    
    def test_group_check_false(self):
        test_user_without_group = User.objects.create_user("test_user2", 'tests2@email.com', "test_password2")
        user_has_group = group_check(test_user_without_group)
        self.assertFalse(user_has_group)
