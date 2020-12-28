from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from django.core import mail


class PasswordTests(APITestCase):

    def setUp(self) -> None:
        self.password = 'tagadatagada'
        self.username = 'user@example.com'
        self.user: User = User.objects.create_user(self.username, self.username, self.password)

    def test_reset_unexisting_user(self):
        """
        Assert no email is being sent if the username is not good
        """
        url = reverse('rest_password_reset')
        data = {
            'email': self.username + 'm',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_existing_user(self):
        """
        Assert that an email has been sent
        """
        response = self._send_reset_form()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def test_reset_existing_user_uppercase(self):
        """
        Assert that an email has been sent
        """
        url = reverse('rest_password_reset')
        data = {
            'email': self.username.upper(),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def _send_reset_form(self):
        url = reverse('rest_password_reset')
        data = {
            'email': self.username,
        }
        response = self.client.post(url, data)
        return response

    def test_reset_password_confirm_wrong_form(self):
        self._send_reset_form()
        url = reverse('rest_password_reset_confirm')
        data = {
            'new_password1': self.password+'m',
            'new_password2': self.password,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': PasswordResetTokenGenerator().make_token(self.user),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_confirm_valid_form(self):
        self._send_reset_form()
        url = reverse('rest_password_reset_confirm')
        data = {
            'new_password1': self.password,
            'new_password2': self.password,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': PasswordResetTokenGenerator().make_token(self.user),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_confirm_valid_form_but_wrong_token(self):
        self._send_reset_form()
        url = reverse('rest_password_reset_confirm')
        data = {
            'new_password1': self.password,
            'new_password2': self.password,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': PasswordResetTokenGenerator().make_token(self.user)+'wrong',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

