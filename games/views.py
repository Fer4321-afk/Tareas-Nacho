import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from django.contrib.auth.decorators import login_required

@login_required
def game_list(request):
    # Si el usuario crea una nueva sala
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        if room_name:
            # Crear juego asignando al creador como player1
            game = Game.objects.create(
                room_name=room_name, 
                owner=request.user,
                player1=request.user  # <-- Asignar como jugador 1
            )
        return redirect('games:list')
    
    # Mostrar todas las salas
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def play_game(request, pk):
    # Buscar el juego por ID
    game = get_object_or_404(Game, pk=pk)
    
    # Asignar jugador 2 si no hay y es diferente al creador
    if not game.player2 and request.user != game.player1:
        game.player2 = request.user
        game.save()
    
    # Si el usuario hace un movimiento (click en casilla)
    if request.method == "POST" and game.state == 'active':
        # Verificar que el usuario puede mover
        if not game.can_move(request.user):
            return redirect('games:play', pk=pk)
        
        # Obtener qué casilla clickeó (0 a 8)
        square_id = int(request.POST.get('square'))
        
        # Convertir el tablero de string a lista
        board_list = list(game.board)
        
        # Solo hacer movimiento si la casilla está vacía
        if board_list[square_id] == ' ':
            # Poner X o O según turno y jugador
            if game.player1 == request.user:
                board_list[square_id] = 'X'
            else:
                board_list[square_id] = 'O'
            
            # Cambiar turno
            game.is_player1_turn = not game.is_player1_turn
            
            # Guardar tablero actualizado
            game.board = ''.join(board_list)
            
            # Verificar si hay ganador
            if game.check_winner():
                game.state = 'won'
                game.winner = request.user
            # Verificar si es empate (tablero lleno)
            elif ' ' not in game.board:
                game.state = 'tie'
            
            # Guardar cambios en base de datos
            game.save()
        
        # Recargar la página para mostrar cambios
        return redirect('games:play', pk=pk)

    # ============================================
    # PREPARAR DATOS PARA WEBSOCKET
    # ============================================
    
    # Definir can_move aquí antes de usarla
    can_move = game.can_move(request.user)
    
    game_data = json.dumps({
        'game_id': game.id,
        'room_name': game.room_name,
        'player': request.user.username,
        'player_id': request.user.id,
        'is_player1': game.player1 == request.user,
        'is_player2': game.player2 == request.user,
        'board': game.board,
        'state': game.state,
        'is_player1_turn': game.is_player1_turn,
        'can_move': can_move 
      
    })
    
    # Mostrar la página del juego CON datos WebSocket
    return render(request, 'games/play_game.html', {
        'game': game,
        'game_data': game_data,
        'can_move': can_move  
    })

@login_required
def delete_game(request, pk):
    # Buscar juego y borrarlo solo si el usuario es el dueño
    game = get_object_or_404(Game, pk=pk)
    if request.user == game.owner:
        game.delete()
    return redirect('games:list')