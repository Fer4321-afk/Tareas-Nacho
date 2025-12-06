import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    # 1. CUANDO UN JUGADOR SE CONECTA
    async def connect(self):
        # Obtenemos el ID de la sala de la URL
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        # Creamos un nombre único para el grupo (todos en la misma sala)
        self.room_group_name = f'game_{self.room_id}'
        
        # Añadimos este cliente al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,  # Nombre del grupo
            self.channel_name      # Identificador único del cliente
        )
        
        # Aceptamos la conexión WebSocket
        await self.accept()
        print(f"✅ Jugador conectado a sala {self.room_id}")
    
    # 2. CUANDO UN JUGADOR SE DESCONECTA
    async def disconnect(self, close_code):
        # Lo removemos del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"❌ Jugador desconectado de sala {self.room_id}")
    
    # 3. CUANDO RECIBIMOS UN MENSAJE (movimiento o chat)
    async def receive(self, text_data):
        # El mensaje viene como JSON: {"type": "move", "square": 4, "player": "Ana"}
        data = json.loads(text_data)
        print(f"📨 Mensaje recibido: {data}")
        
        # Reenviamos el mensaje a TODOS en la misma sala
        await self.channel_layer.group_send(
            self.room_group_name,  # Enviar a este grupo
            {
                'type': 'game_message',  # Qué función ejecutar en cada cliente
                'data': data              # Los datos del mensaje
            }
        )
    
    # 4. FUNCIÓN QUE SE EJECUTA EN CADA CLIENTE DEL GRUPO
    async def game_message(self, event):
        # 'event' contiene los datos que enviamos en group_send()
        # Enviamos el mensaje por el WebSocket a este cliente específico
        await self.send(text_data=json.dumps(event['data']))