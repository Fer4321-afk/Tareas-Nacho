from django.urls import path
from . import views

urlpatterns = [
    path('', views.pokemon_view, name='pokemon_home'),
    path('<str:name>/', views.pokemon_view, name='pokemon_detail'),
]