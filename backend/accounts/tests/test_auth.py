"""
accounts/tests/test_auth.py

Tests for: login, token refresh, logout, protected endpoints, password reset.
These are the critical-path tests required by Milestone 1.
"""

import uuid
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import PasswordResetToken
from accounts.tests.factories import (
    UserFactory,
    InactiveUserFactory,
    PasswordResetTokenFactory,
)


LOGIN_URL = "/api/auth/login/"
REFRESH_URL = "/api/auth/token/refresh/"
LOGOUT_URL = "/api/auth/logout/"
ME_URL = "/api/auth/me/"
PW_RESET_REQUEST_URL = "/api/auth/password-reset/request/"
PW_RESET_CONFIRM_URL = "/api/auth/password-reset/confirm/"


def get_tokens(client, email, password="Str0ng!Pass"):
    resp = client.post(
        LOGIN_URL,
        {"email": email, "password": password},
        content_type="application/json",
    )
    return resp


@pytest.mark.django_db
class TestLogin:

    def test_valid_credentials_return_tokens(self, client):
        user = UserFactory()
        resp = get_tokens(client, user.email)
        assert resp.status_code == 200
        data = resp.json()
        assert "access" in data
        assert "refresh" in data

    def test_login_includes_user_profile(self, client):
        user = UserFactory()
        resp = get_tokens(client, user.email)
        assert "user" in resp.json()
        assert resp.json()["user"]["email"] == user.email

    def test_wrong_password_rejected(self, client):
        user = UserFactory()
        resp = client.post(
            LOGIN_URL, {"email": user.email, "password": "WrongPass!"},
            content_type="application/json",
        )
        assert resp.status_code == 401

    def test_inactive_user_cannot_login(self, client):
        """Unverified user should not receive tokens."""
        user = InactiveUserFactory()
        resp = get_tokens(client, user.email)
        assert resp.status_code in (400, 401)

    def test_unknown_email_rejected(self, client):
        resp = client.post(
            LOGIN_URL, {"email": "nobody@nowhere.com", "password": "AnyPass!"},
            content_type="application/json",
        )
        assert resp.status_code == 401

    def test_role_in_response(self, client):
        user = UserFactory(role="restaurant")
        resp = get_tokens(client, user.email)
        assert resp.json()["user"]["role"] == "restaurant"


@pytest.mark.django_db
class TestTokenRefresh:

    def test_valid_refresh_returns_new_access_token(self, client):
        user = UserFactory()
        tokens = get_tokens(client, user.email).json()
        resp = client.post(
            REFRESH_URL, {"refresh": tokens["refresh"]},
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert "access" in resp.json()

    def test_invalid_refresh_token_rejected(self, client):
        resp = client.post(
            REFRESH_URL, {"refresh": "notavalidtoken"},
            content_type="application/json",
        )
        assert resp.status_code == 401

    def test_new_access_token_works_on_protected_endpoint(self, client):
        """Newly-refreshed access token must be accepted on /me/."""
        user = UserFactory()
        tokens = get_tokens(client, user.email).json()
        refresh_resp = client.post(
            REFRESH_URL, {"refresh": tokens["refresh"]},
            content_type="application/json",
        )
        new_access = refresh_resp.json()["access"]
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {new_access}")
        me_resp = api.get(ME_URL)
        assert me_resp.status_code == 200


@pytest.mark.django_db
class TestLogout:

    def test_logout_blacklists_refresh_token(self, client):
        user = UserFactory()
        tokens = get_tokens(client, user.email).json()
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        logout_resp = api.post(
            LOGOUT_URL, {"refresh": tokens["refresh"]},
            format="json",
        )
        assert logout_resp.status_code == 200
        # Attempting to use the blacklisted refresh token should fail
        refresh_resp = client.post(
            REFRESH_URL, {"refresh": tokens["refresh"]},
            content_type="application/json",
        )
        assert refresh_resp.status_code == 401

    def test_logout_requires_auth(self, client):
        resp = client.post(LOGOUT_URL, {"refresh": "anything"}, content_type="application/json")
        assert resp.status_code == 401

    def test_logout_without_refresh_token_returns_400(self, client):
        user = UserFactory()
        tokens = get_tokens(client, user.email).json()
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        resp = api.post(LOGOUT_URL, {}, format="json")
        assert resp.status_code == 400


@pytest.mark.django_db
class TestProtectedEndpoint:

    def test_me_requires_authentication(self, client):
        resp = client.get(ME_URL)
        assert resp.status_code == 401

    def test_me_with_valid_token(self, client):
        user = UserFactory()
        tokens = get_tokens(client, user.email).json()
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        resp = api.get(ME_URL)
        assert resp.status_code == 200
        assert resp.json()["data"]["email"] == user.email

    def test_me_with_bad_token_returns_401(self, client):
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION="Bearer totallyinvalidtoken")
        resp = api.get(ME_URL)
        assert resp.status_code == 401

    def test_me_patch_updates_profile(self, client):
        user = UserFactory()
        tokens = get_tokens(client, user.email).json()
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        resp = api.patch(ME_URL, {"full_name": "Updated Name"}, format="json")
        assert resp.status_code == 200
        user.refresh_from_db()
        assert user.full_name == "Updated Name"

    def test_me_cannot_change_role(self, client):
        user = UserFactory(role="customer")
        tokens = get_tokens(client, user.email).json()
        api = APIClient()
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        api.patch(ME_URL, {"role": "admin"}, format="json")
        user.refresh_from_db()
        assert user.role == "customer"


@pytest.mark.django_db
class TestPasswordReset:

    def test_reset_request_returns_200_for_existing_email(self, client):
        user = UserFactory()
        with patch("accounts.views.send_password_reset_email"):
            resp = client.post(
                PW_RESET_REQUEST_URL,
                {"email": user.email},
                content_type="application/json",
            )
        assert resp.status_code == 200

    def test_reset_request_returns_200_for_unknown_email(self, client):
        """Should not leak whether an email exists (always 200)."""
        resp = client.post(
            PW_RESET_REQUEST_URL,
            {"email": "nobody@example.com"},
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_reset_token_created_for_active_user(self, client):
        user = UserFactory()
        with patch("accounts.views.send_password_reset_email"):
            client.post(PW_RESET_REQUEST_URL, {"email": user.email}, content_type="application/json")
        assert PasswordResetToken.objects.filter(user=user).exists()

    def test_confirm_valid_token_changes_password(self, client):
        token_obj = PasswordResetTokenFactory()
        new_pass = "NewStr0ng!Pass99"
        resp = client.post(
            PW_RESET_CONFIRM_URL,
            {"token": str(token_obj.token), "new_password": new_pass, "new_password_confirm": new_pass},
            content_type="application/json",
        )
        assert resp.status_code == 200
        # Can now log in with the new password
        login_resp = get_tokens(client, token_obj.user.email, password=new_pass)
        assert login_resp.status_code == 200

    def test_confirm_expired_token_rejected(self, client):
        token_obj = PasswordResetTokenFactory()
        token_obj.expires_at = timezone.now() - timedelta(hours=2)
        token_obj.save()
        new_pass = "NewStr0ng!Pass99"
        resp = client.post(
            PW_RESET_CONFIRM_URL,
            {"token": str(token_obj.token), "new_password": new_pass, "new_password_confirm": new_pass},
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_confirm_used_token_rejected(self, client):
        token_obj = PasswordResetTokenFactory()
        token_obj.used = True
        token_obj.save()
        new_pass = "NewStr0ng!Pass99"
        resp = client.post(
            PW_RESET_CONFIRM_URL,
            {"token": str(token_obj.token), "new_password": new_pass, "new_password_confirm": new_pass},
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_confirm_nonexistent_token_returns_404(self, client):
        new_pass = "NewStr0ng!Pass99"
        resp = client.post(
            PW_RESET_CONFIRM_URL,
            {"token": str(uuid.uuid4()), "new_password": new_pass, "new_password_confirm": new_pass},
            content_type="application/json",
        )
        assert resp.status_code == 404

    def test_confirm_password_mismatch_rejected(self, client):
        token_obj = PasswordResetTokenFactory()
        resp = client.post(
            PW_RESET_CONFIRM_URL,
            {
                "token": str(token_obj.token),
                "new_password": "Str0ng!One",
                "new_password_confirm": "Str0ng!Two",
            },
            content_type="application/json",
        )
        assert resp.status_code == 400
