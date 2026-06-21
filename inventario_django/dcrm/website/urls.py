"""
Módulo de URLs de la aplicación website.
Define las rutas URL y las asocia con las vistas correspondientes.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal que carga la página de inicio
    path('', views.home, name='home'),
    
    # Ruta para iniciar sesión
    path('login/', views.login_user, name='login'),
    
    # Ruta para cerrar sesión
    path('logout/', views.logout_user, name='logout'),
    
    # Ruta para el registro de nuevos usuarios
    path('register/', views.register_user, name='register'),
    path('staff/', views.staff_dashboard, name='staff'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]