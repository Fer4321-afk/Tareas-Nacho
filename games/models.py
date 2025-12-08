from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    room_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    
    # JUGADORES
    player1 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='games_as_player1',
        null=True,
        blank=True
    )
    player2 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='games_as_player2', 
        null=True, 
        blank=True
    )
    
    # TURNO activo
    is_player1_turn = models.BooleanField(default=True)
    
    # TABLERO
    board = models.CharField(max_length=9, default='         ')  # 9 espacios
    
    # ESTADO
    state = models.CharField(max_length=10, default="active")  # active, won, tie
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_games')

    def check_winner(self):
        WIN_PATTERNS = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        board = self.board
        for a,b,c in WIN_PATTERNS:
            if board[a] == board[b] == board[c] and board[a] != " ":
                return True
        return False
    
    def can_move(self, user):
        """Verifica si el usuario puede mover ahora"""
        if self.player1 == user and self.is_player1_turn:
            return True
        if self.player2 == user and not self.is_player1_turn:
            return True
        return False
    
    def make_move(self, position, user):
        """Hace un movimiento si es válido"""
        if not self.can_move(user):
            return False
        
        board_list = list(self.board)
        symbol = 'X' if self.player1 == user else 'O'
        board_list[position] = symbol
        self.board = ''.join(board_list)
        
        # Cambiar turno
        self.is_player1_turn = not self.is_player1_turn
        
        # Verificar ganador
        if self.check_winner():
            self.state = 'won'
            self.winner = user
        elif ' ' not in self.board:
            self.state = 'tie'
        
        self.save()
        return True
    
    def __str__(self):
        players = f"P1: {self.player1.username if self.player1 else 'None'}"
        if self.player2:
            players += f", P2: {self.player2.username}"
        return f"{self.room_name} ({players})"