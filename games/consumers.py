import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Game
from asgiref.sync import sync_to_async


class GameConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.group_name = f"game_{self.room_id}"


        # Unirse al grupo
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )


        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
        position = data.get("position")
        username = data.get("username")


        game = await sync_to_async(Game.objects.select_related("player1", "player2").get)(id=self.room_id)
        user = await sync_to_async(User.objects.get)(username=username)


        player1 = game.player1
        player2 = game.player2


        # Validar turno
        if (game.active_player == 1 and user != game.player1) or \
           (game.active_player == 2 and user != game.player2):
            return


        board = list(game.board)


        # Verificar si la casilla está vacía
        if board[position] == "_":
            if game.active_player == 1:
                board[position] = "X"
                game.active_player = 2
            else:
                board[position] = "O"
                game.active_player = 1


        board_str = "".join(board)
        game.board = board_str


        # Verificar ganador
        result = self.check_winner(board)


        if result == "X":
            game.state = "WIN_P1"
        elif result == "O":
            game.state = "WIN_P2"
        elif result == "TIE":
            game.state = "TIE"


        await sync_to_async(game.save)()


        # Enviar actualización a todos los sockets del grupo
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_update",
                "data": {
                    "board": board_str,
                    "state": game.state,
                    "active_player": game.active_player,
                }
            }
        )


    async def send_update(self, event):
        await self.send(text_data=json.dumps({
            "game_data": event["data"]
        }))


    # Función de check_winner dentro del consumer
    def check_winner(self, board):
        win_positions = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]


        for a, b, c in win_positions:
            if board[a] == board[b] == board[c] and board[a] != "_":
                return board[a]


        if "_" not in board:
            return "TIE"


        return None
