import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import games.routing  # Importamos las rutas WebSocket de nuestra app

# Configuración estándar de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

# Router principal que decide: ¿HTTP o WebSocket?
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # ← Peticiones HTTP normales (vistas Django)
    "websocket": AuthMiddlewareStack(  # ← Conexiones WebSocket (tiempo real)
        URLRouter(
            games.routing.websocket_urlpatterns  # Nuestras rutas específicas
        )
    ),
})