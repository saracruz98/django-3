"""
Módulo de vistas para la aplicación website.
Contiene la lógica para la página principal, el registro de usuarios,
la autenticación (inicio y cierre de sesión) y el dashboard del cliente.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import SignUpForm  # Formulario personalizado para el registro

# Importar modelos de workout para usar en dashboards
from workout.models import Routine, Exercise, Session, Observation
from workout.forms import ObservationForm

def home(request):
    """
    Renderiza la página principal de inicio (home.html).
    
    Args:
        request: El objeto HttpRequest con la petición del cliente.
        
    Returns:
        HttpResponse: Render de la plantilla 'home.html'.
    """
    return render(request, 'home.html', {})

def login_user(request):
    """
    Maneja el proceso de inicio de sesión de los usuarios.

    Autentica al usuario usando el sistema estándar de Django (contraseña hasheada).

    Args:
        request: El objeto HttpRequest. Si el método es POST, se intentará autenticar.

    Returns:
        HttpResponse: Redirección a la página principal ('home') en caso de éxito o fallo,
                      mostrando un mensaje correspondiente.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticación estándar de Django (contraseña hasheada con BCrypt)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "¡Has iniciado sesión!")
            return redirect('home')

        # Si la autenticación falla, mostrar mensaje de error
        messages.error(request, "Credenciales Inválidas")
        return redirect('home')
    else:
        # Si no es POST, redirigir a la página principal
        return redirect('home')

def logout_user(request):
    """
    Maneja el proceso de cierre de sesión de los usuarios.
    
    Args:
        request: El objeto HttpRequest.
        
    Returns:
        HttpResponse: Redirección a la página principal ('home') después de cerrar la sesión.
    """
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect('home')

def register_user(request):
    """
    Maneja el proceso de registro de nuevos usuarios.
    
    Si la petición es POST y el formulario es válido, se crea un nuevo usuario.
    De lo contrario, se muestra el formulario de registro.
    
    Args:
        request: El objeto HttpRequest.
        
    Returns:
        HttpResponse: Redirección a 'home' en caso de registro exitoso, o 
                      renderizado de 'register.html' con el formulario en caso contrario.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso, ahora puedes iniciar sesión")
            return redirect('home')
        else:
            messages.error(request, "Hubo un error en el registro")
            return render(request, 'register.html', {'form': form})
    else:
        # Si no es POST, mostrar un formulario vacío
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

@login_required
def client_dashboard(request):
    """Vista del cliente (rol 'customer').
    Solo los usuarios con rol 'customer' pueden acceder.
    Muestra sus rutinas activas y ejercicios disponibles.
    """
    if getattr(request.user, 'rol', None) != 'customer':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    # Obtener rutinas del cliente
    mis_rutinas = Routine.objects.filter(usuario=request.user, activo=True)
    # Lista de ejercicios disponibles (solo lectura)
    ejercicios = Exercise.objects.all()
    context = {
        'user': request.user,
        'rutinas': mis_rutinas,
        'ejercicios': ejercicios,
    }
    return render(request, 'client_dashboard.html', context)

@login_required
def staff_dashboard(request):
    """Vista del personal (rol 'staff').
    Solo los usuarios con rol 'staff' pueden acceder.
    Permite gestionar usuarios y rutinas de cualquier cliente.
    """
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    # Todas las rutinas y usuarios para gestión
    todas_rutinas = Routine.objects.all()
    todos_usuarios = request.user.__class__.objects.all()
    context = {
        'user': request.user,
        'rutinas': todas_rutinas,
        'usuarios': todos_usuarios,
    }
    return render(request, 'staff_dashboard.html', context)


@login_required
def create_observation(request, session_id):
    """Crear una observación para una sesión (solo staff)."""
    from django.shortcuts import get_object_or_404
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    session = get_object_or_404(Session, id=session_id, entrenador=request.user)
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            obs = form.save(commit=False)
            obs.session = session
            obs.creado_por = request.user
            obs.save()
            messages.success(request, "Observación guardada")
            return redirect('staff_dashboard')
    else:
        form = ObservationForm()
    return render(request, 'create_observation.html', {'form': form, 'session': session})
@login_required
def admin_dashboard(request):
    """Vista de administrador (superuser).
    Solo superusuarios pueden acceder.
    Ofrece estadísticas globales y control total.
    """
    if not request.user.is_superuser:
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    total_usuarios = request.user.__class__.objects.count()
    total_rutinas = Routine.objects.count()
    total_ejercicios = Exercise.objects.count()
    context = {
        'user': request.user,
        'total_usuarios': total_usuarios,
        'total_rutinas': total_rutinas,
        'total_ejercicios': total_ejercicios,
    }
    return render(request, 'admin_dashboard.html', context)
