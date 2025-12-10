from django.db import models
from django.contrib.auth.models import User


GAME_STATES = (
    ('ACTIVE', 'Active'),
    ('WIN_P1', 'Player 1 won'),
    ('WIN_P2', 'Player 2 won'),
    ('TIE', 'Tie'),
)


class Game(models.Model):
    room_name = models.CharField(max_length=50, unique=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1_games')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2_games', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.CharField(max_length=9, default="_________")
    active_player = models.IntegerField(default=1)  # 1 or 2
    state = models.CharField(max_length=10, choices=GAME_STATES, default='ACTIVE')


    def __str__(self):
        return f"{self.room_name} (Owner: {self.owner})"


