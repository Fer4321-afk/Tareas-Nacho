import json
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import IntegrityError
from django.contrib import messages
from .models import Game, ChatMessage

@login_required
def game_list(request):
    """Página principal de juegos - SIN BASE DE DATOS"""
    # Listas vacías por ahora
    context = {
        'active_games': [],
        'waiting_games': [],
    }
    return render(request, 'games/list.html', context)

@login_required
def create_game(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        
        if not room_name:
            messages.error(request, 'El nombre de la sala no puede estar vacío')
            return redirect('rooms')
        
        # Si ya existe, agregar un número
        base_name = room_name
        counter = 1
        
        while Game.objects.filter(room_name=room_name).exists():
            room_name = f"{base_name} ({counter})"
            counter += 1
        
        # Crear la sala
        game = Game.objects.create(
            room_name=room_name,
            created_by=request.user,
            player_x=request.user,
            board="-" * 9,
            current_turn="X"
        )
        
        messages.success(request, f'Sala creada: "{room_name}"')
        return redirect('game_room', game_id=game.id)
    
    return redirect('rooms')

@login_required
def game_room(request, game_id):
    """Sala de juego principal"""
    game = get_object_or_404(Game, id=game_id)
    
    # Si el juego está esperando y hay espacio, unirse como jugador O
    if game.status == 'waiting' and not game.player_o and request.user != game.player_x:
        game.player_o = request.user
        game.status = 'active'
        game.save()
    
    # Preparar datos para el frontend
    game_data = {
        'game_id': game.id,
        'room_name': game.room_name,
        'board': game.get_board_list(),
        'current_turn': game.current_turn,
        'status': game.status,
        'player_x': game.player_x.username if game.player_x else None,
        'player_o': game.player_o.username if game.player_o else None,
        'user': request.user.username,
        'is_player_x': request.user.username == game.player_x.username if game.player_x else False,
        'is_player_o': request.user.username == game.player_o.username if game.player_o else False,
    }
    
    return render(request, 'games/room.html', {
        'game': game,
        'game_data_json': json.dumps(game_data),
        'messages': ChatMessage.objects.filter(game=game)[:20]
    })

def register(request):
    """Registro de usuarios (simple)"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('game_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'games/register.html', {'form': form})