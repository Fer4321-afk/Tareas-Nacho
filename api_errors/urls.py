from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.get_server_status, name='status'),
    path('errors/', views.get_errors, name='errors'),
    path('errors/create/', views.create_error, name='create_error'),
    path('errors/<int:code>/', views.get_error_from_code, name='error_by_code'),
    path('errors/update/<int:id>/', views.error_update_delete, name='error_update_delete'),
    path('demo/', views.api_demo, name='api_demo'),  # ← ESTA LÍNEA ES CLAVE
]