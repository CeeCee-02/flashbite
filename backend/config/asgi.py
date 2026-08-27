"""
ASGI config for FLASHBITE.
Handles HTTP (via Daphne) and WebSockets (via Channels).
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

# Must call get_asgi_application() BEFORE importing channels routing
# so that Django apps are fully loaded.
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack  # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.security.websocket import AllowedHostsOriginValidator  # noqa: E402

import tracking.routing  # noqa: E402  (imported after Django setup)

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(tracking.routing.websocket_urlpatterns)
            )
        ),
    }
)
