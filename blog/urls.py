from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blogpage, name='blogpage'),  # Página del blog
    path('<slug:slug>/', views.personasLista, name="personasLista"),  # Lista de personas   
]
