from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    GAME_STATES = [
        ('waiting', 'Esperando jugador'),
        ('active', 'En juego'),
        ('won_x', 'Ganó X'),
        ('won_o', 'Ganó O'),
        ('tie', 'Empate'),
        ('cancelled', 'Cancelado'),
    ]
    
    room_name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    player_x = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='games_as_x')
    player_o = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='games_as_o')
    current_player = models.CharField(max_length=1, default='X', choices=[('X', 'X'), ('O', 'O')])
    board = models.JSONField(default=list)
    state = models.CharField(max_length=20, choices=GAME_STATES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Game: {self.room_name} ({self.state})"
    
    def get_winner(self):
        """Determina si hay un ganador"""
        board = self.board
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
                return board[combo[0]]
        return None
    
    def is_board_full(self):
        """Verifica si el tablero está lleno"""
        return all(cell != '' for cell in self.board)
    
    def make_move(self, position, player_symbol):
        """Realiza un movimiento en el tablero"""
        if self.state != 'active':
            return False
        
        if self.board[position] != '':
            return False
        
        if player_symbol != self.current_player:
            return False
        
        # Verificar que el jugador actual sea el que hace el movimiento
        if player_symbol == 'X' and self.player_x != self.get_current_user():
            return False
        if player_symbol == 'O' and self.player_o != self.get_current_user():
            return False
        
        self.board[position] = player_symbol
        self.current_player = 'O' if player_symbol == 'X' else 'X'
        
        winner = self.get_winner()
        if winner:
            self.state = 'won_x' if winner == 'X' else 'won_o'
        elif self.is_board_full():
            self.state = 'tie'
        
        return True
    
    def get_current_user(self):
        """Obtiene el usuario actual (simulado)"""
        # En realidad, esto debería venir del request
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.first()