"""
Módulo de vistas para la aplicación website.
Contiene la lógica para la página principal, el registro de usuarios,
la autenticación (inicio y cierre de sesión) y el dashboard del cliente.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from accounts.forms import SignUpForm  # Formulario personalizado para el registro

# Importar modelos de workout para usar en dashboards
from workout.models import Routine, Exercise, Session, Observation, Progress, Recommendation
from workout.forms import ObservationForm, ProgressForm, RoutineForm, AssignRoutineForm, ExerciseForm, SessionForm

def home(request):
    """
    Renderiza la página principal o redirige a los dashboards según el rol del usuario.
    """
    if request.user.is_authenticated:
        role = getattr(request.user, 'rol', None)
        if role == 'customer':
            return redirect('client')
        elif role == 'staff':
            return redirect('staff_dashboard')
        elif role == 'admin' or request.user.is_superuser:
            return redirect('admin_dashboard')
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
            # Redirigir según rol
            role = getattr(user, 'rol', None)
            if role == 'customer':
                return redirect('client')
            elif role == 'staff':
                return redirect('staff_dashboard')
            elif role == 'admin' or user.is_superuser:
                return redirect('admin_dashboard')
            else:
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
    Dashboard premium con estadísticas, gráficas, logros y más.
    """
    if getattr(request.user, 'rol', None) != 'customer':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')

    from django.utils import timezone
    from datetime import timedelta
    import json

    today = timezone.now().date()

    # ── Rutinas del cliente ──
    mis_rutinas = Routine.objects.filter(usuario=request.user, activo=True)
    ejercicios = Exercise.objects.all()

    # ── Progreso físico más reciente ──
    progreso_fisico = Progress.objects.filter(cliente=request.user).order_by('-fecha').first()

    # ── Quick stats ──
    mes_inicio = today.replace(day=1)
    entrenos_mes = Session.objects.filter(
        cliente=request.user, fecha_hora__date__gte=mes_inicio
    ).count()

    # Racha (días consecutivos entrenando)
    sesiones_qs = Session.objects.filter(
        cliente=request.user, fecha_hora__date__lte=today
    ).order_by('-fecha_hora')
    racha = 0
    fecha_actual = today
    for ses in sesiones_qs:
        if ses.fecha_hora.date() == fecha_actual:
            racha += 1
            fecha_actual -= timedelta(days=1)
        else:
            break

    # Objetivo mensual
    objetivo_mensual = 20
    objetivo_percent = min(
        round(entrenos_mes / objetivo_mensual * 100, 1) if objetivo_mensual else 0,
        100,
    )

    # Calorías estimadas (250 kcal/sesión)
    calorias_estimadas = entrenos_mes * 250

    # ── Próxima sesión ──
    proxima_sesion = (
        Session.objects.filter(cliente=request.user, fecha_hora__gt=timezone.now())
        .select_related('entrenador', 'rutina')
        .order_by('fecha_hora')
        .first()
    )

    # ── Rutina del día ──
    rutina_hoy = (
        Routine.objects.filter(usuario=request.user, activo=True)
        .order_by('-fecha_creacion')
        .first()
    )
    ejercicios_hoy = []
    if rutina_hoy:
        ejercicios_hoy = rutina_hoy.ejercicios.select_related('ejercicio').all()

    # ── Datos para gráficas ──
    progresos = list(
        Progress.objects.filter(cliente=request.user, fecha__isnull=False).order_by('fecha')
    )
    fechas = [p.fecha.strftime('%Y-%m-%d') for p in progresos if p.fecha]
    pesos = [float(p.peso) if p.peso else None for p in progresos if p.fecha]
    masa = [float(p.muscle_mass) if p.muscle_mass else None for p in progresos if p.fecha]

    # IMC (BMI) por registro
    chart_bmi = []
    for p in progresos:
        if p.fecha and p.peso and p.altura:
            h = float(p.altura) / 100
            chart_bmi.append(round(float(p.peso) / (h * h), 1) if h > 0 else None)
        else:
            chart_bmi.append(None)

    # IMC actual
    bmi_actual = None
    if progreso_fisico and progreso_fisico.peso and progreso_fisico.altura:
        h = float(progreso_fisico.altura) / 100
        if h > 0:
            bmi_actual = round(float(progreso_fisico.peso) / (h * h), 1)

    # Total entrenamientos (histórico)
    total_entrenamientos = Session.objects.filter(cliente=request.user).count()

    # ── Asistencia semanal (últimas 4 semanas) ──
    semanas_labels = []
    semanas_data = []
    for i in range(3, -1, -1):
        ws = today - timedelta(days=today.weekday() + 7 * i)
        we = ws + timedelta(days=6)
        cnt = Session.objects.filter(
            cliente=request.user, fecha_hora__date__gte=ws, fecha_hora__date__lte=we
        ).count()
        semanas_labels.append(f'Sem {4 - i}')
        semanas_data.append(cnt)

    # ── Sistema de logros ──
    logros = []
    if total_entrenamientos >= 1:
        logros.append({'icon': '🎯', 'titulo': 'Primer entrenamiento', 'desc': 'Completaste tu primer entrenamiento', 'logrado': True})
    else:
        logros.append({'icon': '🎯', 'titulo': 'Primer entrenamiento', 'desc': 'Completa tu primer entrenamiento', 'logrado': False})
    if total_entrenamientos >= 10:
        logros.append({'icon': '💪', 'titulo': '10 entrenamientos', 'desc': '¡10 sesiones completadas!', 'logrado': True})
    else:
        logros.append({'icon': '💪', 'titulo': '10 entrenamientos', 'desc': f'{total_entrenamientos}/10 sesiones', 'logrado': False})
    if racha >= 7:
        logros.append({'icon': '⚡', 'titulo': 'Semana completa', 'desc': '7 días consecutivos entrenando', 'logrado': True})
    else:
        logros.append({'icon': '⚡', 'titulo': 'Semana completa', 'desc': f'{racha}/7 días consecutivos', 'logrado': False})
    if objetivo_percent >= 100:
        logros.append({'icon': '🏆', 'titulo': 'Objetivo mensual', 'desc': '¡Meta del mes alcanzada!', 'logrado': True})
    else:
        logros.append({'icon': '🏆', 'titulo': 'Objetivo mensual', 'desc': f'{objetivo_percent}% completado', 'logrado': False})
    if total_entrenamientos >= 50:
        logros.append({'icon': '🔥', 'titulo': '50 entrenamientos', 'desc': '¡Medio centenar de sesiones!', 'logrado': True})
    if Progress.objects.filter(cliente=request.user).exists():
        logros.append({'icon': '📊', 'titulo': 'Progreso registrado', 'desc': 'Primer registro de progreso', 'logrado': True})

    # ── Observaciones y recomendaciones del entrenador ──
    observaciones = Observation.objects.filter(
        session__cliente=request.user
    ).select_related('creado_por').order_by('-fecha')[:5]
    recomendaciones = Recommendation.objects.filter(
        cliente=request.user
    ).order_by('-fecha')[:5]

    # ── Notificaciones ──
    notificaciones = []
    if rutina_hoy:
        notificaciones.append({'icon': '📋', 'texto': f'Rutina activa: {rutina_hoy.nombre}', 'tipo': 'info'})
    if proxima_sesion:
        notificaciones.append({'icon': '📅', 'texto': 'Tienes un entrenamiento pendiente', 'tipo': 'warning'})
    if progreso_fisico:
        notificaciones.append({'icon': '✅', 'texto': 'Peso registrado correctamente', 'tipo': 'success'})
    if not mis_rutinas.exists():
        notificaciones.append({'icon': '⚠️', 'texto': 'No tienes rutinas asignadas', 'tipo': 'danger'})

    # ── Progreso de masa muscular (barra) ──
    progreso_masa_percent = 0
    if progreso_fisico and progreso_fisico.muscle_mass:
        primer = Progress.objects.filter(
            cliente=request.user, muscle_mass__isnull=False
        ).order_by('fecha').first()
        if primer and primer.muscle_mass:
            ganancia = float(progreso_fisico.muscle_mass) - float(primer.muscle_mass)
            meta = 5.0
            progreso_masa_percent = max(0, min(round(ganancia / meta * 100, 1), 100))

    # ── Historial ──
    historial_entrenamientos = (
        Session.objects.filter(cliente=request.user)
        .select_related('rutina', 'entrenador')
        .order_by('-fecha_hora')[:5]
    )

    context = {
        'user': request.user,
        'rutinas': mis_rutinas,
        'ejercicios': ejercicios,
        'progreso_fisico': progreso_fisico,
        'historial_entrenamientos': historial_entrenamientos,
        'entrenos_mes': entrenos_mes,
        'racha_actual': racha,
        'objetivo_percent': objetivo_percent,
        'objetivo_mensual': objetivo_mensual,
        'calorias_estimadas': calorias_estimadas,
        'proxima_sesion': proxima_sesion,
        'rutina_hoy': rutina_hoy,
        'ejercicios_hoy': ejercicios_hoy,
        'chart_fechas': json.dumps(fechas),
        'chart_pesos': json.dumps(pesos),
        'chart_masa': json.dumps(masa),
        'chart_bmi': json.dumps(chart_bmi),
        'chart_semanas_labels': json.dumps(semanas_labels),
        'chart_semanas_data': json.dumps(semanas_data),
        'bmi_actual': bmi_actual,
        'total_entrenamientos': total_entrenamientos,
        'logros': logros,
        'observaciones': observaciones,
        'recomendaciones': recomendaciones,
        'notificaciones': notificaciones,
        'progreso_masa_percent': progreso_masa_percent,
        'today': today,
    }
    return render(request, 'client_dashboard.html', context)


@login_required
def staff_dashboard(request):
    """Vista del personal (rol 'staff').
    Solo puede administrar clientes asignados.
    """
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    
    # 1. Clientes asignados al entrenador
    clientes_asignados = request.user.clientes_asignados.all()
    
    # 2. Rutinas creadas por este entrenador (en las cuales él es el 'usuario' creador o están asignadas a sus clientes)
    # Según los modelos actuales, la rutina tiene un 'usuario' (que originalmente era el cliente). 
    # Para obtener rutinas creadas / asignadas a sus clientes:
    rutinas_clientes = Routine.objects.filter(usuario__in=clientes_asignados, activo=True)
    
    # 3. Sesiones programadas para hoy
    from django.utils import timezone
    today = timezone.now().date()
    sesiones_hoy = Session.objects.filter(
        entrenador=request.user,
        fecha_hora__date=today
    ).select_related('cliente', 'rutina').order_by('fecha_hora')
    
    # 4. Clientes que no han entrenado esta semana
    # Buscamos clientes que no tengan ninguna sesión 'completada' en los últimos 7 días
    hace_una_semana = timezone.now() - timezone.timedelta(days=7)
    clientes_inactivos = []
    for cliente in clientes_asignados:
        entrenado = Session.objects.filter(
            cliente=cliente, 
            estado='completada', 
            fecha_hora__gte=hace_una_semana
        ).exists()
        if not entrenado:
            clientes_inactivos.append(cliente)

    context = {
        'user': request.user,
        'clientes_asignados': clientes_asignados,
        'rutinas_clientes': rutinas_clientes,
        'sesiones_hoy': sesiones_hoy,
        'clientes_inactivos': clientes_inactivos,
    }
    return render(request, 'staff_dashboard.html', context)

@login_required
def create_routine(request):
    """Crear una nueva rutina (solo staff)."""
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.save()
            messages.success(request, "Rutina creada exitosamente")
            return redirect('staff_dashboard')
    else:
        form = RoutineForm()
    return render(request, 'form_template.html', {
        'title': 'Crear Nueva Rutina',
        'form': form,
        'cancel_url': reverse('staff_dashboard'),
    })

@login_required
def assign_routine(request):
    """Asignar una rutina existente a un cliente (solo staff)."""
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    if request.method == 'POST':
        form = AssignRoutineForm(request.POST)
        if form.is_valid():
            # Se asume que el formulario incluye los campos 'rutina' y 'cliente'
            rutina = form.cleaned_data['rutina']
            cliente = form.cleaned_data['cliente']
            rutina.usuario = cliente
            rutina.save()
            messages.success(request, "Rutina asignada al cliente")
            return redirect('staff_dashboard')
    else:
        form = AssignRoutineForm()
    return render(request, 'form_template.html', {
        'title': 'Asignar Rutina a Cliente',
        'form': form,
        'cancel_url': reverse('staff_dashboard'),
    })


@login_required
def create_observation(request, session_id=None):
    """Crear una observación para una sesión (solo staff). Opcionalmente vincula a una sesión mediante session_id."""
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            obs = form.save(commit=False)
            obs.creado_por = request.user
            if session_id:
                try:
                    obs.session = Session.objects.get(pk=session_id)
                except Session.DoesNotExist:
                    messages.error(request, "Sesión no encontrada")
                    return redirect('staff')
            obs.save()
            messages.success(request, "Observación guardada")
            return redirect('staff')
    else:
        form = ObservationForm()
    return render(request, 'observation_form.html', {'form': form})

# Exercise CRUD (staff only)
@login_required
def exercise_list(request):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    ejercicios = Exercise.objects.all()
    return render(request, 'exercise_list.html', {'ejercicios': ejercicios})

@login_required
def exercise_create(request):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ejercicio creado")
            return redirect('exercise_list')
    else:
        form = ExerciseForm()
    return render(request, 'form_template.html', {
        'title': 'Crear ejercicio',
        'form': form,
        'cancel_url': reverse('exercise_list'),
    })

@login_required
def exercise_edit(request, pk):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    ejercicio = Exercise.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=ejercicio)
        if form.is_valid():
            form.save()
            messages.success(request, "Ejercicio actualizado")
            return redirect('exercise_list')
    else:
        form = ExerciseForm(instance=ejercicio)
    return render(request, 'form_template.html', {
        'title': 'Editar ejercicio',
        'form': form,
        'cancel_url': reverse('exercise_list'),
    })

@login_required
def exercise_delete(request, pk):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    ejercicio = Exercise.objects.get(pk=pk)
    ejercicio.delete()
    messages.success(request, "Ejercicio eliminado")
    return redirect('exercise_list')

# Routine CRUD (staff only)
@login_required
def routine_list(request):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    rutinas = Routine.objects.all()
    return render(request, 'routine_list.html', {'rutinas': rutinas})

@login_required
def routine_create(request):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.usuario = request.user
            rutina.save()
            messages.success(request, "Rutina creada")
            return redirect('routine_list')
    else:
        form = RoutineForm()
    return render(request, 'form_template.html', {
        'title': 'Crear rutina',
        'form': form,
        'cancel_url': reverse('routine_list'),
    })

@login_required
def routine_edit(request, pk):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    rutina = Routine.objects.get(pk=pk)
    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, "Rutina actualizada")
            return redirect('routine_list')
    else:
        form = RoutineForm(instance=rutina)
    return render(request, 'form_template.html', {
        'title': 'Editar rutina',
        'form': form,
        'cancel_url': reverse('routine_list'),
    })

@login_required
def routine_delete(request, pk):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    rutina = Routine.objects.get(pk=pk)
    rutina.delete()
    messages.success(request, "Rutina eliminada")
    return redirect('routine_list')

# Progress list & edit (customer)
@login_required
def progress_list(request):
    if getattr(request.user, 'rol', None) != 'customer':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    progresos = Progress.objects.filter(cliente=request.user)
    return render(request, 'progress_list.html', {'progresos': progresos})

@login_required
def progress_edit(request, pk):
    if getattr(request.user, 'rol', None) != 'customer':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    prog = Progress.objects.get(pk=pk, cliente=request.user)
    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=prog)
        if form.is_valid():
            form.save()
            messages.success(request, "Progreso actualizado")
            return redirect('progress_list')
    else:
        form = ProgressForm(instance=prog)
    return render(request, 'form_template.html', {
        'title': 'Editar progreso',
        'form': form,
        'cancel_url': reverse('progress_list'),
    })

# Session CRUD (staff)
@login_required
def session_list(request):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    sesiones = Session.objects.all()
    return render(request, 'session_list.html', {'sesiones': sesiones})

@login_required
def session_edit(request, pk):
    if getattr(request.user, 'rol', None) != 'staff':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    sesion = Session.objects.get(pk=pk)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=sesion)
        if form.is_valid():
            form.save()
            messages.success(request, "Sesión actualizada")
            return redirect('session_list')
    else:
        form = SessionForm(instance=sesion)
    return render(request, 'form_template.html', {
        'title': 'Editar sesión',
        'form': form,
        'cancel_url': reverse('session_list'),
    })

# ---------------------------------------------------------------------------
# End of CRUD placeholders
# ---------------------------------------------------------------------------


@login_required
def add_progress(request):
    """Permite a un cliente registrar su progreso físico (peso y altura)."""
    if getattr(request.user, 'rol', None) != 'customer':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            prog = form.save(commit=False)
            prog.cliente = request.user
            prog.save()
            messages.success(request, "Progreso guardado correctamente")
            return redirect('client')
    else:
        form = ProgressForm()
    return render(request, 'add_progress.html', {'form': form})
@login_required
def admin_dashboard(request):
    """Vista de administrador (superuser o rol admin)."""
    if not request.user.is_superuser and getattr(request.user, 'rol', None) != 'admin':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
        
    User = request.user.__class__
    total_clientes = User.objects.filter(rol='customer').count()
    total_entrenadores = User.objects.filter(rol='staff').count()
    total_rutinas = Routine.objects.filter(activo=True).count()
    total_sesiones = Session.objects.count()
    
    entrenadores_lista = User.objects.filter(rol='staff').prefetch_related('clientes_asignados')
    clientes_lista = User.objects.filter(rol='customer').select_related('entrenador_asignado')

    context = {
        'user': request.user,
        'total_clientes': total_clientes,
        'total_entrenadores': total_entrenadores,
        'total_rutinas': total_rutinas,
        'total_sesiones': total_sesiones,
        'entrenadores_lista': entrenadores_lista,
        'clientes_lista': clientes_lista,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def admin_create_user(request):
    """Crear usuarios (staff o customer)."""
    if not request.user.is_superuser and getattr(request.user, 'rol', None) != 'admin':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
        
    if request.method == 'POST':
        from accounts.forms import SignUpForm
        form = SignUpForm(request.POST)
        if form.is_valid():
            nuevo_user = form.save()
            messages.success(request, f"Usuario {nuevo_user.username} creado exitosamente como {nuevo_user.get_rol_display()}.")
            return redirect('admin_dashboard')
    else:
        from accounts.forms import SignUpForm
        form = SignUpForm()
        
    return render(request, 'form_template.html', {
        'title': 'Crear Nuevo Usuario',
        'form': form,
        'cancel_url': reverse('admin_dashboard'),
    })

@login_required
def admin_assign_trainer(request):
    """Asignar entrenadores a usuarios."""
    if not request.user.is_superuser and getattr(request.user, 'rol', None) != 'admin':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
        
    from accounts.models import CustomUser
    from django import forms

    class AssignTrainerForm(forms.Form):
        cliente = forms.ModelChoiceField(queryset=CustomUser.objects.filter(rol='customer'), label="Seleccionar Cliente")
        entrenador = forms.ModelChoiceField(queryset=CustomUser.objects.filter(rol='staff'), required=False, label="Seleccionar Entrenador (Dejar vacío para remover asignación)")
    
    if request.method == 'POST':
        form = AssignTrainerForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            entrenador = form.cleaned_data['entrenador']
            cliente.entrenador_asignado = entrenador
            cliente.save()
            
            estado = "asignado" if entrenador else "removido"
            messages.success(request, f"Entrenador {estado} para el cliente {cliente.username}.")
            return redirect('admin_dashboard')
    else:
        form = AssignTrainerForm()
        
    return render(request, 'form_template.html', {
        'title': 'Asignar Entrenador a Cliente',
        'form': form,
        'cancel_url': reverse('admin_dashboard'),
    })

@login_required
def admin_manage_exercises(request):
    return redirect('exercise_list')

@login_required
def admin_manage_plans(request):
    return redirect('routine_list')



@login_required
def history(request):
    """Muestra el historial completo de entrenamientos del cliente."""
    if getattr(request.user, 'rol', None) != 'customer':
        messages.error(request, "Acceso no autorizado")
        return redirect('home')
    sesiones = Session.objects.filter(cliente=request.user).order_by('-fecha_hora')
    return render(request, 'history.html', {'sesiones': sesiones})
