import urllib.parse

from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.shortcuts import redirect
from django.urls import reverse
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


class GoogleLogin(SocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        # use the same callback url as defined in your GitHub app, this url
        # must be absolute:
        return self.request.build_absolute_uri(reverse('google_callback'))


def google_callback(request):
    params = urllib.parse.urlencode(request.GET)
    base_url = settings.FRONT_END.get('BASE_URL')
    path = settings.FRONT_END.get('FRONT_OAUTH_PATH', 'oauth')
    return redirect(f'{base_url}/{path}/?{params}')


def reset_password(request):
    base_url = settings.FRONT_END.get('BASE_URL')
    path = settings.FRONT_END.get('FRONT_RESET_PWD_PATH')
    return redirect(f'{base_url}/{path}/')
