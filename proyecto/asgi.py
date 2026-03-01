# proyecto/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# PRIMERO: configurar settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

# SEGUNDO: inicializar Django ASGI
django_asgi_app = get_asgi_application()

# TERCERO: importar routing DESPUÉS de inicializar Django
from games.routing import websocket_urlpatterns

# CUARTO: configurar el router
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
