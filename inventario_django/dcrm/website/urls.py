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
    path('client/', views.client_dashboard, name='client'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('progress/add/', views.add_progress, name='add_progress'),


    
    # Ruta para cerrar sesión
    path('logout/', views.logout_user, name='logout'),
    
    # Ruta para el registro de nuevos usuarios
    path('register/', views.register_user, name='register'),

    path('routine/create/', views.create_routine, name='create_routine'),
    path('routine/assign/', views.assign_routine, name='assign_routine'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create_user/', views.admin_create_user, name='admin_create_user'),
    path('admin/assign_trainer/', views.admin_assign_trainer, name='admin_assign_trainer'),
    path('admin/manage_exercises/', views.admin_manage_exercises, name='admin_manage_exercises'),
    # CRUD for Exercise (staff only)
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/<int:pk>/edit/', views.exercise_edit, name='exercise_edit'),
    path('exercises/<int:pk>/delete/', views.exercise_delete, name='exercise_delete'),
    # CRUD for Routine (staff only)
    path('routines/', views.routine_list, name='routine_list'),
    path('routines/create/', views.routine_create, name='routine_create'),
    path('routines/<int:pk>/edit/', views.routine_edit, name='routine_edit'),
    path('routines/<int:pk>/delete/', views.routine_delete, name='routine_delete'),
    # CRUD for Progress (customer)
    path('progress/', views.progress_list, name='progress_list'),
    path('progress/<int:pk>/edit/', views.progress_edit, name='progress_edit'),
    # CRUD for Session (staff)
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<int:pk>/edit/', views.session_edit, name='session_edit'),
    path('admin/manage_plans/', views.admin_manage_plans, name='admin_manage_plans'),
    path('observation/create/', views.create_observation, name='create_observation'),
    path('observation/create/<int:session_id>/', views.create_observation, name='create_observation'),
    path('history/', views.history, name='history'),

]