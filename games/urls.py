from django.urls import path
from . import views

app_name = "games"

urlpatterns = [
    path('', views.game_list, name='list'),
    path('play/<int:pk>/', views.play_game, name='play'),
    path('delete/<int:pk>/', views.delete_game, name='delete'),
]
