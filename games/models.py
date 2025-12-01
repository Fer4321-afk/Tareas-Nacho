from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    room_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    board = models.CharField(max_length=9, default='         ')  # 9 espacios
 # 9 espacios vacíos
    active_player = models.IntegerField(default=1)  # 1=X, 2=O
    state = models.CharField(max_length=10, default="active")
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
