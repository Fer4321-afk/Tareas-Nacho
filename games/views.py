from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game

@login_required
def game_list(request):
    games = Game.objects.all()
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        if room_name and not Game.objects.filter(room_name=room_name).exists():
            Game.objects.create(room_name=room_name, owner=request.user)
        return redirect('games:game_list')
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    board = list(game.board)

    # Eliminar partida terminada si el owner lo solicita
    if request.method == "POST" and "delete" in request.POST and request.user == game.owner:
        game.delete()
        return redirect('games:game_list')

    # Solo el dueño puede jugar
    if request.method == "POST" and request.user == game.owner and game.state == "active":
        move = int(request.POST.get("move"))
        if board[move] == ' ':
            board[move] = 'X' if game.active_player == 1 else 'O'
            game.board = ''.join(board)
            game.active_player = 2 if game.active_player == 1 else 1

            # Comprobar ganador
            combos = [
                [0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]
            ]
            for a,b,c in combos:
                if board[a] == board[b] == board[c] != ' ':
                    game.state = 'won'
                    game.winner = board[a]
                    break
            if ' ' not in board and game.state == 'active':
                game.state = 'tie'

            game.save()

    return render(request, 'games/play_game.html', {'game': game})
