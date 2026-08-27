# config/__init__.py
# Make config a package so `celery -A config` works.
from .celery import app as celery_app  # noqa: F401

__all__ = ("celery_app",)
