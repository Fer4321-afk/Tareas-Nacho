from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('create/', views.create_game, name='create_game'),
    path('game/<str:room_name>/', views.game_detail, name='game_detail'),
    path('game/<str:room_name>/delete/', views.delete_game, name='delete_game'),
    path('api/game/<str:room_name>/move/', views.make_move_api, name='make_move_api'),
]