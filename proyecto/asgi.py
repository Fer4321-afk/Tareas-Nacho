# proyecto/asgi.py - REEMPLAZA TODO

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from games.routing import websocket_urlpatterns  # ¡Importante desde TU app!

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

# Aplicación ASGI principal
application = ProtocolTypeRouter({
    # Para peticiones HTTP normales
    "http": get_asgi_application(),
    
    # Para conexiones WebSocket
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})