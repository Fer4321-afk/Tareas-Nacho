from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Game as GameModel

def join_game(request, juego_id):
    try:
        game = GameModel.objects.get(id=juego_id)
    except GameModel.DoesNotExist:
        return HttpResponseNotFound("Juego no encontrado")

    # Si ya existe jugador 2 → no permitir unirse
    if game.jugador2:
        return redirect('ver_juego', juego_id=game.id)

    from .models import Usuario  # si tu modelo de usuario es ese

    # Asignar jugador2 automáticamente
    user = Usuario.objects.first()  # pon aquí el usuario real si usas login
    game.jugador2 = user
    game.save()

    return redirect('ver_juego', juego_id=game.id)
