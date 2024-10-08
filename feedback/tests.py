from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

def create_user(user_dict:dict):
    """ Create user """
    UserModel = get_user_model()
    username = user_dict.get('username')
    if not UserModel.objects.filter(username=username).exists():
        user = UserModel.objects.create_user(username, password=user_dict.get('password'))
        user.email = user_dict.get('email')
        user.first_name = user_dict.get('first_name')
        user.last_name = user_dict.get('last_name')
        user.is_superuser = user_dict.get('superuser', False)
        user.is_staff = user_dict.get('superuser', False)
        user.save()

def create_admin_user():
    """ Create Admin user """
    users = [{
        'username': 'admin',
        'password': 'admin1',
        'first_name': 'Admin',
        'last_name': 'Person',
        'email': 'admin@example.com',
        'superuser': True,
    }]
    for user in users:
        create_user(user)

def create_test_user():
    """ Create Foo user """
    users = [{
        'username': 'foo',
        'password': 'bar1',
        'first_name': 'Foo',
        'last_name': 'Bar',
        'email': 'foo@example.com',
        'superuser': False,
    }]
    for user in users:
        create_user(user)

def create_second_test_user():
    """ Create Foo2 user """
    users = [{
        'username': 'foo2',
        'password': 'bar2',
        'first_name': 'Foo2',
        'last_name': 'Bar2',
        'email': 'foo2@example.com',
        'superuser': False,
    }]
    for user in users:
        create_user(user)

def get_user(username:str = 'foo'):
    """ Get user """
    UserModel = get_user_model()
    return UserModel.objects.filter(username=username).first()

class IndexUserViewTests(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.client.login(username='foo', password='bar1')

    def test_index(self):
        response = self.client.get(reverse("feedback:root"))
        self.assertEqual(response.status_code, 302)

class IndexAdminViewTests(TestCase):
    def setUp(self):
        self.user = create_admin_user()
        self.client.login(username='admin', password='admin1')

    def test_index(self):
        response = self.client.get(reverse("feedback:root"))
        self.assertEqual(response.status_code, 302)
