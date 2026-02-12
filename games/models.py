# games/models.py
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player2', null=True, blank=True)
    board = models.CharField(max_length=9, default="         ")
    current_turn = models.CharField(max_length=1, default='X')
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=1, null=True, blank=True)
    
    def __str__(self):
        return f"{self.room_name} - {self.player1} vs {self.player2}"
    
    def make_move(self, position, player):
        if not self.active:
            return False, "Partida terminada", None
        if self.winner:
            return False, f"Ganó {self.winner}", None
        if player != self.current_turn:
            return False, "No es tu turno", None
        
        board_list = list(self.board)
        if position < 0 or position > 8 or board_list[position] != ' ':
            return False, "Casilla inválida", None
        
        board_list[position] = player
        self.board = ''.join(board_list)
        
        winner = self.check_winner()
        if winner:
            self.winner = winner
            self.active = False
            self.save()
            return True, f"¡Gana {winner}!", winner
        
        if ' ' not in self.board:
            self.active = False
            self.save()
            return True, "Empate", None
        
        self.current_turn = 'O' if player == 'X' else 'X'
        self.save()
        return True, "Movimiento OK", None
    
    def check_winner(self):
        b = self.board
        lines = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for line in lines:
            if b[line[0]] == b[line[1]] == b[line[2]] != ' ':
                return b[line[0]]
        return None
    
    def reset_board(self):
        self.board = "         "
        self.current_turn = 'X'
        self.winner = None
        self.active = True
        self.save()