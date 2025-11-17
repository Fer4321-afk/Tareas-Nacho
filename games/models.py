from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.CharField(max_length=9, default=' ' * 9)  # 9 casillas vacías
    active_player = models.IntegerField(default=1)  # 1 o 2
    state = models.CharField(max_length=20, default='active')  # active / won / tie
    winner = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.room_name
