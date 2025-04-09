from django.urls import include, path

from identities.views.basic_login import BasicLoginAPI
from identities.views.google_login import GoogleLoginAPI
from identities.views.register import RegisterAPI
from identities.views.profile import ProfileAPI

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path("login/", BasicLoginAPI.as_view(), name="basic-login-api"),
    path("register/", RegisterAPI.as_view(), name="register-api"),
    path("profile/", ProfileAPI.as_view(), name="profile-api"),
    path("social/google/", GoogleLoginAPI.as_view(), name="google-login-api"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
