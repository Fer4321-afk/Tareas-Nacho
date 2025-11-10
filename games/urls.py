from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('<int:game_id>/', views.play_game, name='play_game'),
]
