# games/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Game

def lista_partidas(request):
    games = Game.objects.filter(active=True).order_by('-id')
    return render(request, 'games/lista_partidas.html', {'games': games})

@login_required
def crear_partida(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if Game.objects.filter(room_name=room_name).exists():
            messages.error(request, 'Ya existe')
            return redirect('games:crear_partida')
        game = Game.objects.create(room_name=room_name, player1=request.user)
        messages.success(request, f'Sala {room_name} creada')
        return redirect('games:sala', game_id=game.id)
    return render(request, 'games/crear_partida.html')

@login_required
def unirse_partida(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if game.player2:
        messages.error(request, 'Sala llena')
        return redirect('games:lista_partidas')
    if game.player1 == request.user:
        messages.error(request, 'Ya eres el creador')
        return redirect('games:sala', game_id=game.id)
    game.player2 = request.user
    game.save()
    messages.success(request, f'Te uniste a {game.room_name}')
    return redirect('games:sala', game_id=game.id)

@login_required
def sala(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if request.user not in [game.player1, game.player2] and game.player2 is not None:
        messages.error(request, 'No eres parte')
        return redirect('games:lista_partidas')
    
    if request.user == game.player1:
        player_symbol = 'X'
    elif request.user == game.player2:
        player_symbol = 'O'
    else:
        player_symbol = None
    
    context = {
        'game': game,
        'board': list(game.board),
        'player_symbol': player_symbol,
        'es_player1': request.user == game.player1,
    }
    return render(request, 'games/sala.html', context)

@login_required
def cerrar_partida(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.user == game.player1:
        game.delete()
        messages.success(request, 'Partida eliminada')
    return redirect('games:lista_partidas')