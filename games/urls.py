from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_juegos, name='lista_juegos'),
    path('crear/', views.crear_juego, name='crear_juego'),
    path('new/', views.crear_juego, name='game_new'),

    # Ver detalle del juego
    path('<int:juego_id>/', views.ver_juego, name='ver_juego'),

    # Hacer movimiento
    path('<int:juego_id>/mover/', views.hacer_movimiento, name='hacer_movimiento'),

    # Eliminar juego
    path('<int:juego_id>/eliminar/', views.eliminar_juego, name='eliminar_juego'),

    # Unirse como jugador 2
    path('<int:juego_id>/join/', views.join_game, name='game_join'),
]
