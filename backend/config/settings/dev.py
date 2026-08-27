"""
Development settings.
Usage: DJANGO_SETTINGS_MODULE=config.settings.dev
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Dev: allow all CORS origins for convenience
CORS_ALLOW_ALL_ORIGINS = True

# Dev: use Django in-memory cache (no Redis required to start hacking)
# Switch to Redis by setting REDIS_URL in .env and using channels_redis layer (already configured in base)

# Dev: relax throttling so automated tests aren't rate-limited
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {  # noqa: F405
    "anon": "1000/day",
    "user": "10000/day",
    "auth": "100/min",
    "password_reset": "100/hour",
}

# Dev: print emails to console if RESEND_API_KEY is not set
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Dev: Django extensions
INSTALLED_APPS = INSTALLED_APPS + ["django_extensions"]  # noqa: F405
