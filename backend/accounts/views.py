"""
accounts/views.py

All authentication API views.
Each endpoint returns the standard FLASHBITE JSON envelope via core.exceptions.success_response.
"""

import logging

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.exceptions import success_response
from .emails import send_verification_email, send_password_reset_email
from .models import User, EmailVerificationToken, PasswordResetToken
from .serializers import (
    RegisterSerializer,
    EmailVerifySerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer,
    CustomTokenObtainPairSerializer,
)
from .throttles import AuthRateThrottle, PasswordResetThrottle

logger = logging.getLogger("flashbite")


# ── Register ───────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
@throttle_classes([AuthRateThrottle])
def register(request):
    """
    POST /api/auth/register/
    Body: { email, full_name, phone?, role, password, password_confirm }
    Creates a new inactive user and sends a verification email.
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    # Create verification token and send email
    token_obj = EmailVerificationToken.objects.create(user=user)
    frontend_base = _get_frontend_base()
    try:
        send_verification_email(user, str(token_obj.token), base_url=frontend_base)
    except Exception:
        # Non-fatal: user can request re-send (future feature). Log and continue.
        logger.exception("Verification email failed for %s", user.email)

    return success_response(
        data={"email": user.email, "role": user.role},
        message="Account created. Please check your email to verify your address.",
        status_code=status.HTTP_201_CREATED,
    )


# ── Email Verification ─────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def verify_email(request):
    """
    POST /api/auth/verify-email/
    Body: { token: "<uuid>" }
    Marks the user's email as verified and activates the account.
    """
    serializer = EmailVerifySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        token_obj = EmailVerificationToken.objects.select_related("user").get(
            token=serializer.validated_data["token"]
        )
    except EmailVerificationToken.DoesNotExist:
        return Response(
            {"success": False, "error": "NotFound", "message": "Invalid verification token."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not token_obj.is_valid():
        return Response(
            {
                "success": False,
                "error": "BadRequest",
                "message": "This verification link has expired or already been used.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = token_obj.user
    user.is_active = True
    user.save(update_fields=["is_active"])

    token_obj.used = True
    token_obj.save(update_fields=["used"])

    return success_response(message="Email verified successfully. You can now log in.")


# ── Login ──────────────────────────────────────────────────────────────────────

class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Returns access + refresh JWT tokens plus user profile.
    Throttled at 5 req/min.
    """
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [AuthRateThrottle]


# ── Token Refresh ──────────────────────────────────────────────────────────────
# Handled by rest_framework_simplejwt.views.TokenRefreshView (registered in urls.py)


# ── Logout ─────────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    POST /api/auth/logout/
    Body: { refresh: "<refresh_token>" }
    Blacklists the refresh token (requires rest_framework_simplejwt.token_blacklist).
    """
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"success": False, "error": "BadRequest", "message": "Refresh token is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError as exc:
        return Response(
            {"success": False, "error": "BadRequest", "message": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return success_response(message="Logged out successfully.")


# ── Password Reset Request ─────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
@throttle_classes([PasswordResetThrottle])
def password_reset_request(request):
    """
    POST /api/auth/password-reset/request/
    Body: { email }
    Sends a password reset email if the account exists.
    Always returns 200 to prevent email enumeration.
    """
    serializer = PasswordResetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    try:
        user = User.objects.get(email=email, is_active=True)
        token_obj = PasswordResetToken.objects.create(user=user)
        frontend_base = _get_frontend_base()
        send_password_reset_email(user, str(token_obj.token), base_url=frontend_base)
    except User.DoesNotExist:
        # Silently succeed to prevent email enumeration
        pass
    except Exception:
        logger.exception("Password reset email failed for %s", email)

    return success_response(
        message="If an account with that email exists, a reset link has been sent."
    )


# ── Password Reset Confirm ─────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def password_reset_confirm(request):
    """
    POST /api/auth/password-reset/confirm/
    Body: { token, new_password, new_password_confirm }
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        token_obj = PasswordResetToken.objects.select_related("user").get(
            token=serializer.validated_data["token"]
        )
    except PasswordResetToken.DoesNotExist:
        return Response(
            {"success": False, "error": "NotFound", "message": "Invalid reset token."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not token_obj.is_valid():
        return Response(
            {
                "success": False,
                "error": "BadRequest",
                "message": "This reset link has expired or already been used.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = token_obj.user
    user.set_password(serializer.validated_data["new_password"])
    user.save(update_fields=["password"])

    token_obj.used = True
    token_obj.save(update_fields=["used"])

    # Invalidate all other reset tokens for this user
    PasswordResetToken.objects.filter(user=user, used=False).update(used=True)

    return success_response(message="Password reset successful. You can now log in.")


# ── User Profile ───────────────────────────────────────────────────────────────

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    """
    GET  /api/auth/me/  — return current user profile
    PATCH /api/auth/me/ — update full_name or phone
    """
    if request.method == "GET":
        serializer = UserProfileSerializer(request.user)
        return success_response(data=serializer.data)

    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success_response(data=serializer.data, message="Profile updated.")


# ── Utilities ──────────────────────────────────────────────────────────────────

def _get_frontend_base() -> str:
    """Return frontend base URL from CORS_ALLOWED_ORIGINS, or localhost fallback."""
    cors_origins = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
    for origin in cors_origins:
        if origin.startswith("https://"):
            return origin
    return "http://localhost:3000"
