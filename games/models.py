from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    code = models.CharField(max_length=10)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_p1')
    player2 = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='rooms_p2')
    created = models.DateTimeField(auto_now_add=True)
