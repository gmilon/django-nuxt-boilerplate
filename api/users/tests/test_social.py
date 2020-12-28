import responses

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestSocialAuth(APITestCase):
    USERNAME = 'person@world.com'
    PASS = 'person'
    EMAIL = "person1@world.com"
    REGISTRATION_DATA = {
        "username": USERNAME,
        "password1": PASS,
        "password2": PASS,
        "email": EMAIL
    }

    def setUp(self):
        social_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='123123123',
            secret='321321321',
        )
        site = Site.objects.get_current()
        social_app.sites.add(site)
        self.google_url = 'http://google.com/foobarme'

    def _get_url(self):
        url = reverse('google_url')
        return self.client.get(url)

    def test_google_sign_in_url(self):
        response = self._get_url()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('https://accounts.google.com/o/oauth2/auth', response.url)

    def test_failed_social_auth(self):
        url = reverse('google_login')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(
        FRONT_END={
            'BASE_URL': 'http://localhost:3000',
            'OAUTH_PATH': 'oauth',
            'FRONT_RESET_PWD_PATH': 'reset-password',
        }
    )
    def test_google_callback(self):
        url = reverse('google_callback')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    @responses.activate
    def test_social_auth(self):
        responses.add(
            responses.POST,
            'https://accounts.google.com/o/oauth2/token',
            json={'access_token': 'test-code'},
            status=201,
        )
        responses.add(
            responses.GET,
            'https://www.googleapis.com/oauth2/v1/userinfo?access_token=test-code&alt=json',
            json={
                'id': 123,
                'email': 'test@tagada.com',
                'family_name': 'testfamily',
                'given_name': 'given_name'
            },
            status=200,
        )
        url = reverse('google_login')
        response = self.client.post(url, {
            'code': 'test-code',
            'state': 'test-state',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data.keys())
