from django.urls import path, include
from users.views import GoogleLogin, google_callback, google_views, reset_password

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('allauth/', include('allauth.urls'), name='socialaccount_signup'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='password_reset_confirm'),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/url/', google_views.oauth2_login, name='google_url'),
]
