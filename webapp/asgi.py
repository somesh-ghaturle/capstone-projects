"""
ASGI config for FAIR-Agent Web Application

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import fair_agent_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            fair_agent_app.routing.websocket_urlpatterns
        )
    ),
})