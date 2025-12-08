# games/consumers.py - COPIA Y PEGA ESTO

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    """
    Consumer básico para Tic Tac Toe.
    Por ahora solo hace eco para probar la conexión.
    """
    
    async def connect(self):
        """Cuando un cliente se conecta"""
        print("🟢 [CONSUMER] Cliente intentando conectar...")
        
        # Aceptar la conexión
        await self.accept()
        print("✅ [CONSUMER] Cliente CONECTADO")
        
        # Enviar mensaje de bienvenida
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'message': '¡Conectado al juego!'
        }))

    async def disconnect(self, close_code):
        """Cuando un cliente se desconecta"""
        print(f"🔴 [CONSUMER] Cliente desconectado. Código: {close_code}")

    async def receive(self, text_data):
        """Cuando recibimos un mensaje del cliente"""
        try:
            # Parsear los datos JSON
            data = json.loads(text_data)
            print(f"📩 [CONSUMER] Mensaje recibido: {data}")
            
            # Responder con eco (solo para prueba)
            response = {
                'type': 'echo',
                'received': data,
                'message': 'Mensaje recibido correctamente'
            }
            
            await self.send(text_data=json.dumps(response))
            
        except json.JSONDecodeError:
            # Si no es JSON válido
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Formato JSON inválido'
            }))