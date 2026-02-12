# games/urls.py
from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.lista_partidas, name='lista_partidas'),
    path('crear/', views.crear_partida, name='crear_partida'),
    path('unirse/<int:game_id>/', views.unirse_partida, name='unirse_partida'),
    path('sala/<int:game_id>/', views.sala, name='sala'),
    path('cerrar/<int:game_id>/', views.cerrar_partida, name='cerrar_partida'),
]