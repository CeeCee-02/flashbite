"""accounts URL patterns."""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    register,
    verify_email,
    LoginView,
    logout,
    password_reset_request,
    password_reset_confirm,
    me,
)

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("verify-email/", verify_email, name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", logout, name="logout"),
    path("password-reset/request/", password_reset_request, name="password-reset-request"),
    path("password-reset/confirm/", password_reset_confirm, name="password-reset-confirm"),
    path("me/", me, name="me"),
]
