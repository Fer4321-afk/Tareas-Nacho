import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("✅ WebSocket conectado")
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"📩 Mensaje: {data}")
        await self.send(json.dumps({
            'type': 'chat',
            'message': f"Recibí: {data.get('text', '')}"
        }))