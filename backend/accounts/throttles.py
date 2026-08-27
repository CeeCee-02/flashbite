"""
accounts/throttles.py

Custom DRF throttle classes for auth endpoints.
Stricter than the global defaults — prevents brute-force and abuse.
"""

from rest_framework.throttling import AnonRateThrottle


class AuthRateThrottle(AnonRateThrottle):
    """5 requests/minute on register and login (unauthenticated)."""
    scope = "auth"


class PasswordResetThrottle(AnonRateThrottle):
    """3 requests/hour on password reset request."""
    scope = "password_reset"
