from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class SignUpTests(APITestCase):

    def setUp(self) -> None:
        self.password = 'tagada'
        self.validpassword = 'tagadatagada'
        self.username = 'user@example.com'
        self.user: User = User.objects.create_user(self.username, self.username, self.password)

    def test_register_existing_user(self):
        url = reverse('rest_register')
        data = {
            'username': self.username,
            'email': self.username,
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_match(self):
        url = reverse('rest_register')
        data = {
            'username': self.username,
            'email': self.username,
            'password1': self.password,
            'password2': self.password+'nope',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_no_email(self):
        url = reverse('rest_register')
        data = {
            'username': self.username,
            'password1': self.password,
            'password2': self.password+'nope',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_email_null(self):
        url = reverse('rest_register')
        data = {
            'username': self.username,
            'email': None,
            'password1': self.password,
            'password2': self.password+'nope',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_username_null(self):
        url = reverse('rest_register')
        data = {
            'username': None,
            'email': self.username,
            'password1': self.password,
            'password2': self.password+'nope',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_valid_form(self):
        url = reverse('rest_register')
        username = self.username+'c'
        data = {
            'username': username,
            'email': username,
            'password1': self.validpassword,
            'password2': self.validpassword,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username=username).exists(), True)

    def test_register_short_password(self):
        url = reverse('rest_register')
        data = {
            'username': self.username+'c',
            'email': self.username+'c',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_username_is_not_email(self):
        url = reverse('rest_register')
        data = {
            'username': 'notanemail',
            'email': self.username+'no',
            'password1': self.validpassword,
            'password2': self.validpassword,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
