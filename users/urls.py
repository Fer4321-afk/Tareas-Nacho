from django.urls import path
from . import views

app_name = 'users '  # <-- Esto define el namespace que usas en tu href

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # otras URLs si las hay
]
