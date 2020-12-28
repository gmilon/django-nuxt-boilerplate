from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class SignInTests(APITestCase):

    def setUp(self) -> None:
        self.password = 'tagada'
        self.username = 'user@example.com'
        self.user: User = User.objects.create_user(self.username, self.username, self.password)

    def test_sign_in_wrong_username(self):
        """
            Ensure a user cannot sign in if he enter wrong username
        """
        url = reverse('rest_login')
        data = {
            'username': self.username + 'wrong',
            'password': self.password,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_wrong_password(self):
        """
            Ensure a user cannot sign in if he enter wrong username
        """
        url = reverse('rest_login')
        data = {
            'username': self.username,
            'password': self.password + 'wrong',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_right_credentials(self):
        """
            Ensure a user cannot sign in if he enter wrong username
        """
        url = reverse('rest_login')
        data = {
            'username': self.user.username,
            'password': self.password,
        }
        response = self.client.post(url, data, format='json')
        token = getattr(self.user, 'auth_token', None)
        self.assertNotEqual(type(token), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data.get('key', None)), str)
        self.assertEqual(response.data.get('key', None), token.key)

