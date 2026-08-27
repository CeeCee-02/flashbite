"""
accounts/emails.py

Email sending via Resend SDK.
Falls back to logging the link to the console if RESEND_API_KEY is not set,
so local development works without a verified domain.
"""

import logging
from django.conf import settings

logger = logging.getLogger("flashbite")


def _send_via_resend(to: str, subject: str, html: str) -> None:
    """Send an email via the Resend SDK. Raises on failure."""
    import resend  # imported lazily to avoid import error if package not installed in test

    resend.api_key = settings.RESEND_API_KEY
    resend.Emails.send(
        {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [to],
            "subject": subject,
            "html": html,
        }
    )


def _send_or_log(to: str, subject: str, html: str, log_link: str = "") -> None:
    """
    Send email if RESEND_API_KEY is configured.
    Otherwise, log the link to console (dev fallback).
    """
    if settings.RESEND_API_KEY:
        try:
            _send_via_resend(to, subject, html)
            logger.info("Email sent to %s — subject: %s", to, subject)
        except Exception as exc:
            logger.error("Failed to send email to %s: %s", to, exc)
            raise
    else:
        logger.warning(
            "[DEV — no RESEND_API_KEY] Email not sent to %s. %s",
            to,
            f"Link: {log_link}" if log_link else f"Subject: {subject}",
        )


# ── Public helpers ─────────────────────────────────────────────────────────────

def send_verification_email(user, token: str, base_url: str = "http://localhost:3000") -> None:
    """Send the email verification link to a newly registered user."""
    verify_url = f"{base_url}/verify-email?token={token}"
    html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
      <h2>Welcome to FLASHBITE, {user.full_name}!</h2>
      <p>Please verify your email address to activate your account.</p>
      <p>
        <a href="{verify_url}"
           style="background:#FF6B35; color:white; padding:12px 24px;
                  border-radius:6px; text-decoration:none; display:inline-block;">
          Verify Email
        </a>
      </p>
      <p>This link expires in 24 hours.</p>
      <p>If you didn't create a FLASHBITE account, you can safely ignore this email.</p>
      <hr/>
      <small>FLASHBITE · Abuja, Nigeria</small>
    </div>
    """
    _send_or_log(
        to=user.email,
        subject="Verify your FLASHBITE email address",
        html=html,
        log_link=verify_url,
    )


def send_password_reset_email(user, token: str, base_url: str = "http://localhost:3000") -> None:
    """Send password reset link to user."""
    reset_url = f"{base_url}/reset-password?token={token}"
    html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
      <h2>Reset your FLASHBITE password</h2>
      <p>Hi {user.full_name},</p>
      <p>We received a request to reset your password. Click the button below:</p>
      <p>
        <a href="{reset_url}"
           style="background:#FF6B35; color:white; padding:12px 24px;
                  border-radius:6px; text-decoration:none; display:inline-block;">
          Reset Password
        </a>
      </p>
      <p>This link expires in 1 hour.</p>
      <p>If you didn't request a password reset, you can safely ignore this email.</p>
      <hr/>
      <small>FLASHBITE · Abuja, Nigeria</small>
    </div>
    """
    _send_or_log(
        to=user.email,
        subject="Reset your FLASHBITE password",
        html=html,
        log_link=reset_url,
    )
