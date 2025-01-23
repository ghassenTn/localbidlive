"""
ASGI config for localbidlive project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "localbidlive.settings")

django_asgi_app = get_asgi_application()

from auctions import routing as auction_routing  # noqa

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                auction_routing.websocket_urlpatterns
            )
        )
    ),
})
