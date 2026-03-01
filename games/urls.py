from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('create/', views.create_game, name='create_game'),
    path('room/<int:game_id>/', views.game_room, name='game_room'),
    path('login/', auth_views.LoginView.as_view(template_name='games/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]