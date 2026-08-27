"""
Production settings.
Usage: DJANGO_SETTINGS_MODULE=config.settings.prod
"""

from .base import *  # noqa: F401, F403

DEBUG = False

# Celery Beat — installed in prod environment
try:
    import django_celery_beat  # noqa: F401
    INSTALLED_APPS = INSTALLED_APPS + ["django_celery_beat"]  # noqa: F405
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
except ImportError:
    pass

# Security hardening
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "flashbite": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
