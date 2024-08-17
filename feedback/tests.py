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
        user.is_superuser = False
        user.is_staff = False
        user.save()

def create_test_user():
    """ Create Foo user """
    users = [{
        'username': 'foo',
        'password': 'bar',
        'first_name': 'Foo',
        'last_name': 'Bar',
        'email': 'foo@example.com',
        }]
    for user in users:
        create_user(user)

def create_second_test_user():
    users = [{
        'username': 'foo2',
        'password': 'bar2',
        'first_name': 'Foo2',
        'last_name': 'Bar2',
        'email': 'foo2@example.com',
        }]
    for user in users:
        create_user(user)

def get_user():
    """ Get user """
    UserModel = get_user_model()
    return UserModel.objects.filter(username='foo').first()

class IndexViewTests(TestCase):
    # def setUp(self):
        # self.user = create_test_user()
        # self.client.login(username='foo', password='bar')

    def test_index(self):
        response = self.client.get(reverse("feedback:root"))
        self.assertEqual(response.status_code, 200)
