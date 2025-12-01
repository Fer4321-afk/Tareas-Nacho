from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from django.contrib.auth.decorators import login_required

@login_required
def game_list(request):
    # Si el usuario crea una nueva sala
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        if room_name:
            Game.objects.create(room_name=room_name, owner=request.user)
        return redirect('games:list')
    
    # Mostrar todas las salas
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def play_game(request, pk):
    # Buscar el juego por ID
    game = get_object_or_404(Game, pk=pk)

    # Si el usuario hace un movimiento (click en casilla)
    if request.method == "POST" and game.state == 'active':
        # Obtener qué casilla clickeó (0 a 8)
        square_id = int(request.POST.get('square'))
        
        # Convertir el tablero de string a lista: "   " -> [" ", " ", " "]
        board_list = list(game.board)
        
        # Solo hacer movimiento si la casilla está vacía
        if board_list[square_id] == ' ':
            # Poner X o O según turno
            if game.active_player == 1:
                board_list[square_id] = 'X'
                game.active_player = 2  # Cambiar turno a O
            else:
                board_list[square_id] = 'O'
                game.active_player = 1  # Cambiar turno a X
            
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

    # Mostrar la página del juego
    return render(request, 'games/play_game.html', {'game': game})

@login_required
def delete_game(request, pk):
    # Buscar juego y borrarlo solo si el usuario es el dueño
    game = get_object_or_404(Game, pk=pk)
    if request.user == game.owner:
        game.delete()
    return redirect('games:list')