import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game, ChatMessage

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected#15")
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = f'game_{self.game_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print("WebSocket connected#16")
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['type'] == 'move':
            await self.handle_move(data)
        elif data['type'] == 'chat':
            await self.handle_chat(data)
    
    async def handle_move(self, data):
        game = await self.get_game()
        board = game.get_board_list()
        position = data['position']
        player = data['player']
        
        # Verificar movimiento válido
        if (board[position] == ' ' and 
            ((player == 'X' and self.scope['user'].username == game.player_x.username) or
             (player == 'O' and self.scope['user'].username == game.player_o.username))):
            
            board[position] = player
            game.set_board_list(board)
            
            # Cambiar turno
            game.current_turn = 'O' if player == 'X' else 'X'
            
            # Verificar si hay ganador
            winner = game.check_winner()
            if winner:
                game.status = 'finished' if winner != 'draw' else 'draw'
                game.winner = winner if winner != 'draw' else None
            
            await self.save_game(game)
            
            # Enviar actualización a todos
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_update',
                    'board': board,
                    'current_turn': game.current_turn,
                    'status': game.status,
                    'winner': game.winner,
                }
            )
    
    async def handle_chat(self, data):
        game = await self.get_game()
        user = self.scope['user']
        
        # Guardar mensaje en base de datos
        await self.save_message(game, user, data['message'])
        
        # Enviar a todos en la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': user.username,
                'message': data['message'],
                'timestamp': str(user.username)  # Simplificado
            }
        )
    
    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'board': event['board'],
            'current_turn': event['current_turn'],
            'status': event['status'],
            'winner': event.get('winner'),
        }))
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'user': event['user'],
            'message': event['message'],
        }))
    
    @database_sync_to_async
    def get_game(self):
        return Game.objects.get(id=self.game_id)
    
    @database_sync_to_async
    def save_game(self, game):
        game.save()
    
    @database_sync_to_async
    def save_message(self, game, user, message):
        ChatMessage.objects.create(game=game, user=user, message=message)