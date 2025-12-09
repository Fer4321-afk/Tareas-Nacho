import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.group = f'room_{self.room_code}'
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['type'] == 'chat':
            await self.channel_layer.group_send(self.group, {
                'type': 'chat_message',
                'message': data['message'],
                'user': data['user']
            })
        elif data['type'] == 'move':
            await self.channel_layer.group_send(self.group, {
                'type': 'game_move',
                'position': data['position'],
                'player': data['player']
            })

    async def chat_message(self, event):
        await self.send(json.dumps(event))

    async def game_move(self, event):
        await self.send(json.dumps(event))