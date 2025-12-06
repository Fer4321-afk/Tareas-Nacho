from django.urls import re_path
from . import consumers  # Importamos el "consumidor" que maneja la lógica

# Patrones de URL para WebSockets (similar a urlpatterns en urls.py)
websocket_urlpatterns = [
    # Ejemplo: ws://localhost:8000/ws/game/5/ → sala con ID 5
    re_path(r'ws/game/(?P<room_id>\w+)/$', consumers.GameConsumer.as_asgi()),
]