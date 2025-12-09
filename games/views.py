from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def game_list(request):
    return render(request, 'games/index.html')

@login_required
def game_room(request, room_code):
    return render(request, 'games/room.html', {
        'room_code': room_code,
        'username': request.user.username
    })