import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Game

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'
        
        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Enviar estado actual del juego
        game = await self.get_game()
        if game:
            await self.send_game_state(game)
    
    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'move':
            await self.handle_move(data)
        elif action == 'chat':
            await self.handle_chat(data)
        elif action == 'join':
            await self.handle_join(data)
    
    async def handle_move(self, data):
        """Manejar movimiento"""
        position = data.get('position')
        player_symbol = data.get('player')
        
        # Obtener juego desde la base de datos
        game = await self.get_game()
        if not game:
            return
        
        # Verificar usuario
        user = self.scope.get('user')
        if isinstance(user, AnonymousUser):
            return
        
        # Verificar que el usuario sea un jugador
        if player_symbol == 'X' and game.player_x != user:
            return
        if player_symbol == 'O' and game.player_o != user:
            return
        
        # Realizar movimiento
        success = await sync_to_async(game.make_move)(position, player_symbol)
        if success:
            await sync_to_async(game.save)()
            
            # Enviar actualización a todos en la sala
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_update',
                    'game_state': {
                        'board': game.board,
                        'current_player': game.current_player,
                        'state': game.state,
                        'player_x': game.player_x.username if game.player_x else None,
                        'player_o': game.player_o.username if game.player_o else None,
                    }
                }
            )
    
    async def handle_chat(self, data):
        """Manejar mensajes del chat"""
        message = data.get('message')
        user = self.scope.get('user')
        username = user.username if not isinstance(user, AnonymousUser) else 'Anónimo'
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
    
    async def handle_join(self, data):
        """Manejar unión de jugadores"""
        game = await self.get_game()
        if game:
            await self.send_game_state(game)
    
    async def game_update(self, event):
        """Enviar actualización del juego"""
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'data': event['game_state']
        }))
    
    async def chat_message(self, event):
        """Enviar mensaje del chat"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'username': event['username'],
            'message': event['message']
        }))
    
    async def send_game_state(self, game):
        """Enviar estado actual del juego"""
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'data': {
                'room_name': game.room_name,
                'board': game.board,
                'current_player': game.current_player,
                'state': game.state,
                'player_x': game.player_x.username if game.player_x else None,
                'player_o': game.player_o.username if game.player_o else None,
            }
        }))
    
    @sync_to_async
    def get_game(self):
        """Obtener juego desde la base de datos"""
        try:
            return Game.objects.get(room_name=self.room_name)
        except Game.DoesNotExist:
            return None