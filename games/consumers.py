# games/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sala_id = self.scope['url_route']['kwargs']['sala_id']
        self.sala_group = f'sala_{self.sala_id}'
        
        await self.channel_layer.group_add(self.sala_group, self.channel_name)
        await self.accept()
        print(f"✅ WebSocket conectado a sala {self.sala_id}")
        
        self.game = await self.get_game(self.sala_id)
        await self.enviar_estado()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.sala_group, self.channel_name)
        print(f"❌ WebSocket desconectado de sala {self.sala_id}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        accion = data['accion']
        print(f"📩 Acción recibida: {accion}")
        
        if accion == 'movimiento':
            await self.procesar_movimiento(data)
        elif accion == 'chat':
            await self.channel_layer.group_send(
                self.sala_group,
                {
                    'type': 'mensaje_chat',
                    'usuario': data['usuario'],
                    'mensaje': data['mensaje']
                }
            )
        elif accion == 'reiniciar':
            await self.reset_game()
            await self.enviar_estado()

    async def procesar_movimiento(self, data):
        pos = data['posicion']
        jugador = data['jugador']
        
        success, msg, winner = await self.make_move(pos, jugador)
        
        if success:
            await self.channel_layer.group_send(
                self.sala_group,
                {
                    'type': 'actualizar_tablero',
                    'board': self.game.board,
                    'current_turn': self.game.current_turn,
                    'winner': self.game.winner,
                    'active': self.game.active
                }
            )

    async def actualizar_tablero(self, event):
        await self.send(text_data=json.dumps({
            'type': 'estado',
            'board': event['board'],
            'current_turn': event['current_turn'],
            'winner': event['winner'],
            'active': event['active']
        }))

    async def mensaje_chat(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'usuario': event['usuario'],
            'mensaje': event['mensaje']
        }))

    async def enviar_estado(self):
        await self.send(text_data=json.dumps({
            'type': 'estado',
            'board': self.game.board,
            'current_turn': self.game.current_turn,
            'winner': self.game.winner,
            'active': self.game.active
        }))

    @database_sync_to_async
    def get_game(self, sala_id):
        return Game.objects.get(id=sala_id)

    @database_sync_to_async
    def make_move(self, position, player):
        return self.game.make_move(position, player)

    @database_sync_to_async
    def reset_game(self):
        self.game.reset_board()