import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
import games.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": games.routing.websocket_urlpatterns,
})