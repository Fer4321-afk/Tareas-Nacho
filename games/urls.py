from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('create/', views.create_room, name='create_room'),
    path('room/<str:room_code>/', views.game_room, name='game_room'),
]