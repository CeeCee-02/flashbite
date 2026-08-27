"""
accounts/tests/test_email_verify.py

Tests for POST /api/auth/verify-email/
Covers: valid token, expired token, already-used token, invalid UUID.
"""

import uuid
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from accounts.models import EmailVerificationToken
from accounts.tests.factories import InactiveUserFactory, EmailVerificationTokenFactory


VERIFY_URL = "/api/auth/verify-email/"


@pytest.mark.django_db
class TestEmailVerify:

    def test_valid_token_activates_user(self, client):
        """A valid token should set is_active=True on the user."""
        token_obj = EmailVerificationTokenFactory()
        resp = client.post(VERIFY_URL, {"token": str(token_obj.token)}, content_type="application/json")
        assert resp.status_code == 200
        token_obj.user.refresh_from_db()
        assert token_obj.user.is_active is True

    def test_valid_token_is_marked_used(self, client):
        """Token should be marked used after successful verification."""
        token_obj = EmailVerificationTokenFactory()
        client.post(VERIFY_URL, {"token": str(token_obj.token)}, content_type="application/json")
        token_obj.refresh_from_db()
        assert token_obj.used is True

    def test_valid_token_returns_success(self, client):
        token_obj = EmailVerificationTokenFactory()
        resp = client.post(VERIFY_URL, {"token": str(token_obj.token)}, content_type="application/json")
        assert resp.json()["success"] is True

    def test_already_used_token_rejected(self, client):
        """A token that has already been used should return 400."""
        token_obj = EmailVerificationTokenFactory()
        token_obj.used = True
        token_obj.save()
        resp = client.post(VERIFY_URL, {"token": str(token_obj.token)}, content_type="application/json")
        assert resp.status_code == 400
        assert resp.json()["success"] is False

    def test_expired_token_rejected(self, client):
        """A token past its expiry should return 400."""
        token_obj = EmailVerificationTokenFactory()
        token_obj.expires_at = timezone.now() - timedelta(hours=1)
        token_obj.save()
        resp = client.post(VERIFY_URL, {"token": str(token_obj.token)}, content_type="application/json")
        assert resp.status_code == 400

    def test_nonexistent_token_returns_404(self, client):
        """A random UUID that doesn't exist should return 404."""
        resp = client.post(VERIFY_URL, {"token": str(uuid.uuid4())}, content_type="application/json")
        assert resp.status_code == 404

    def test_invalid_uuid_returns_400(self, client):
        """Garbage token string should return 400 (serializer validation)."""
        resp = client.post(VERIFY_URL, {"token": "not-a-uuid"}, content_type="application/json")
        assert resp.status_code == 400
