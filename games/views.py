from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from django.contrib.auth.decorators import login_required

@login_required
def game_list(request):
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        if room_name:
            Game.objects.create(room_name=room_name, owner=request.user)
            return redirect('games:list')
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def play_game(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == "POST" and game.state == 'active':
        square_id = int(request.POST.get('square'))
        board = list(game.board)
        token = 'X' if game.active_player == 1 else 'O'

        if board[square_id] == ' ':
            board[square_id] = token
            game.board = ''.join(board)
            if game.check_winner():
                game.state = 'won'
                game.winner = request.user
            elif ' ' not in board:
                game.state = 'tie'
            else:
                game.active_player = 2 if game.active_player == 1 else 1
            game.save()
        return redirect('games:play', pk=pk)

    return render(request, 'games/play_game.html', {'game': game})

@login_required
def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.user == game.owner:
        game.delete()
    return redirect('games:list')