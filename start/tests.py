from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Group, AnonymousUser
from django.urls import reverse


class TestUserLoginLogout(TestCase):
    def setUp(self):
        self.client = Client()

        self.username = 'test_user'
        self.password = 'test_password'
        
        user = User.objects.create_user(self.username, 'tests@email.com', self.password)
        Group.objects.get_or_create(name='Weaeinkauf')
        weaeinkauf_group = Group.objects.get(name='Weaeinkauf')
        user.groups.add(weaeinkauf_group)
        return super().setUp()
    
    def test_user_login(self):
        response = self.client.post(reverse('login'), {"username": self.username, "password": self.password}, content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 200)
    
    def test_user_register(self):
        response = self.client.post(reverse('logout'), content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

