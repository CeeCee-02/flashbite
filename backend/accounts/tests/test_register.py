"""
accounts/tests/test_register.py

Tests for POST /api/auth/register/
Covers: all 3 public roles, duplicate email, invalid role, password mismatch,
        missing fields, token creation, email send (mocked).
"""

import uuid
from unittest.mock import patch

import pytest

from accounts.models import User, EmailVerificationToken, UserRole


REGISTER_URL = "/api/auth/register/"
VALID_PAYLOAD = {
    "email": "test@example.com",
    "full_name": "Test User",
    "phone": "08012345678",
    "role": "customer",
    "password": "Str0ng!Pass99",
    "password_confirm": "Str0ng!Pass99",
}


@pytest.mark.django_db
class TestRegister:
    def _post(self, client, payload=None):
        data = {**VALID_PAYLOAD, **(payload or {})}
        return client.post(REGISTER_URL, data, content_type="application/json")

    # ── Happy paths ────────────────────────────────────────────────────────────

    @pytest.mark.parametrize("role", ["customer", "restaurant", "rider"])
    def test_register_all_public_roles(self, client, role):
        """All three public roles should register successfully."""
        with patch("accounts.views.send_verification_email"):
            resp = self._post(client, {"email": f"{role}@example.com", "role": role})
        assert resp.status_code == 201
        assert resp.json()["success"] is True
        assert User.objects.filter(email=f"{role}@example.com").exists()

    def test_user_inactive_after_register(self, client):
        """User should be inactive until email is verified."""
        with patch("accounts.views.send_verification_email"):
            self._post(client)
        user = User.objects.get(email=VALID_PAYLOAD["email"])
        assert user.is_active is False

    def test_verification_token_created(self, client):
        """An EmailVerificationToken should be created on register."""
        with patch("accounts.views.send_verification_email"):
            self._post(client)
        user = User.objects.get(email=VALID_PAYLOAD["email"])
        assert EmailVerificationToken.objects.filter(user=user).exists()

    def test_verification_email_called(self, client):
        """send_verification_email should be called once on successful register."""
        with patch("accounts.views.send_verification_email") as mock_send:
            self._post(client)
        mock_send.assert_called_once()

    # ── Validation errors ──────────────────────────────────────────────────────

    def test_duplicate_email_rejected(self, client):
        """Second registration with same email returns 400."""
        with patch("accounts.views.send_verification_email"):
            self._post(client)
            resp = self._post(client)
        assert resp.status_code == 400
        assert resp.json()["success"] is False

    def test_admin_role_rejected(self, client):
        """Role=admin should be rejected."""
        resp = self._post(client, {"role": "admin"})
        assert resp.status_code == 400

    def test_invalid_role_rejected(self, client):
        """Unknown role string should be rejected."""
        resp = self._post(client, {"role": "supervillain"})
        assert resp.status_code == 400

    def test_password_mismatch_rejected(self, client):
        resp = self._post(client, {"password_confirm": "DifferentPass99!"})
        assert resp.status_code == 400
        assert "password" in str(resp.json()).lower()

    def test_weak_password_rejected(self, client):
        resp = self._post(client, {"password": "123", "password_confirm": "123"})
        assert resp.status_code == 400

    def test_missing_email_rejected(self, client):
        data = {k: v for k, v in VALID_PAYLOAD.items() if k != "email"}
        resp = client.post(REGISTER_URL, data, content_type="application/json")
        assert resp.status_code == 400

    def test_missing_role_rejected(self, client):
        data = {k: v for k, v in VALID_PAYLOAD.items() if k != "role"}
        resp = client.post(REGISTER_URL, data, content_type="application/json")
        assert resp.status_code == 400

    def test_email_normalised_to_lowercase(self, client):
        """Email should be stored lowercase regardless of input case."""
        with patch("accounts.views.send_verification_email"):
            self._post(client, {"email": "UPPER@EXAMPLE.COM"})
        assert User.objects.filter(email="upper@example.com").exists()
