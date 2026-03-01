from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Esperando jugador'),
        ('active', 'En juego'),
        ('finished', 'Terminado'),
        ('draw', 'Empate'),
    ]
    
    room_name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_created')
    player_x = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_x', null=True, blank=True)
    player_o = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_o', null=True, blank=True)
    current_turn = models.CharField(max_length=1, default='X')
    board = models.CharField(max_length=9, default=' ' * 9)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    winner = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.room_name} ({self.status})"
    
    def get_board_list(self):
        return list(self.board)
    
    def set_board_list(self, board_list):
        self.board = ''.join(board_list)
    
    def check_winner(self):
        board = self.get_board_list()
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in win_combinations:
            a, b, c = combo
            if board[a] != ' ' and board[a] == board[b] == board[c]:
                return board[a]
        
        if ' ' not in board:
            return 'draw'
        
        return None

class ChatMessage(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}..."