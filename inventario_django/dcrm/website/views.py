"""
Módulo de vistas para la aplicación website.
Contiene la lógica para la página principal, el registro de usuarios,
y la autenticación (inicio y cierre de sesión).
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import SignUpForm  # Formulario personalizado para el registro

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
