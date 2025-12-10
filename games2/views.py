from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Game
from django.contrib.auth.models import User

@login_required
def game_list(request):
    """Lista de juegos activos"""
    active_games = Game.objects.filter(state__in=['waiting', 'active'])
    user_games = Game.objects.filter(player_x=request.user) | Game.objects.filter(player_o=request.user)
    
    return render(request, 'games/index.html', {
        'active_games': active_games,
        'user_games': user_games,
    })

@login_required
def create_game(request):
    """Crear un nuevo juego"""
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        
        if Game.objects.filter(room_name=room_name).exists():
            messages.error(request, 'Ya existe una sala con ese nombre')
            return redirect('game_list')
        
        # Crear el tablero vacío
        board = ['' for _ in range(9)]
        
        game = Game.objects.create(
            room_name=room_name,
            owner=request.user,
            player_x=request.user,
            board=board,
            state='waiting'
        )
        
        messages.success(request, f'Juego "{room_name}" creado exitosamente')
        return redirect('game_detail', room_name=room_name)
    
    return redirect('game_list')

@login_required
def game_detail(request, room_name):
    """Detalle del juego"""
    game = get_object_or_404(Game, room_name=room_name)
    
    # Si el juego está esperando y hay un segundo jugador disponible
    if game.state == 'waiting' and not game.player_o and request.user != game.player_x:
        game.player_o = request.user
        game.state = 'active'
        game.save()
    
    # Verificar si el usuario actual es jugador
    is_player = request.user in [game.player_x, game.player_o]
    is_owner = request.user == game.owner
    
    # Preparar datos para el frontend
    game_data = {
        'room_name': game.room_name,
        'board': game.board,
        'current_player': game.current_player,
        'state': game.state,
        'player_x': game.player_x.username if game.player_x else None,
        'player_o': game.player_o.username if game.player_o else None,
        'is_player': is_player,
        'is_owner': is_owner,
        'current_user': request.user.username,
    }
    
    return render(request, 'games/game.html', {
        'game': game,
        'game_data': json.dumps(game_data),
    })

@login_required
def delete_game(request, room_name):
    """Eliminar un juego"""
    game = get_object_or_404(Game, room_name=room_name)
    
    if request.user == game.owner:
        game.delete()
        messages.success(request, 'Juego eliminado')
    
    return redirect('game_list')

@csrf_exempt
@login_required
def make_move_api(request, room_name):
    """API para realizar movimientos (para HTTP tradicional)"""
    if request.method == 'POST':
        game = get_object_or_404(Game, room_name=room_name)
        data = json.loads(request.body)
        
        position = data.get('position')
        player = data.get('player')
        
        if game.make_move(position, player):
            game.save()
            return JsonResponse({
                'success': True,
                'board': game.board,
                'current_player': game.current_player,
                'state': game.state,
            })
    
    return JsonResponse({'success': False})