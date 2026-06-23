"""
Módulo de Formularios (Workout)
Implementación intensiva del Principio DRY (Don't Repeat Yourself) mediante Patrón Factory (ModelForm).
Delega la validación y creación de campos de interfaz a la configuración de los Modelos de la BD.
"""

from django import forms
from django.contrib.auth import get_user_model
from workout.models import Observation, Progress, Routine, Exercise, Session, ClientExerciseLog

class ObservationForm(forms.ModelForm):
    """Formulario para que un Staff agregue observaciones a una sesión."""
    class Meta:
        model = Observation
        fields = ['session', 'texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe la observación aquí...'}),
        }

class ProgressForm(forms.ModelForm):
    """Formulario para registro de progreso de clientes. Hereda validaciones numéricas del modelo."""
    class Meta:
        model = Progress
        fields = ['peso', 'altura']
        widgets = {
            'peso': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Peso en kg'}),
            'altura': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Altura en cm'}),
        }

class RoutineForm(forms.ModelForm):
    """
    Formulario de creación de Rutinas.
    Se inyecta la restricción de que el queryset de 'usuario' solo muestre perfiles con rol 'customer'.
    """
    class Meta:
        model = Routine
        fields = ['nombre', 'descripcion', 'usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Fuerza Superior, Piernas, etc.'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ej. Rutina enfocada en hipertrofia y fuerza...'}),
        }
        labels = {
            'nombre': 'Nombre de la Rutina',
            'descripcion': 'Descripción detallada',
            'usuario': 'Asignar a Cliente',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrado de base de datos para asignar rutinas únicamente a Clientes
        self.fields['usuario'].queryset = get_user_model().objects.filter(rol='customer')

class AssignRoutineForm(forms.Form):
    """Formulario estándar (No ModelForm) para asignar dinámicamente rutinas existentes a clientes."""
    rutina = forms.ModelChoiceField(queryset=Routine.objects.all(), label='Rutina')
    cliente = forms.ModelChoiceField(queryset=get_user_model().objects.filter(rol='customer'), label='Cliente')

class ExerciseForm(forms.ModelForm):
    """Formulario CRUD para Ejercicios."""
    class Meta:
        model = Exercise
        fields = ['nombre', 'descripcion', 'duracion_min', 'dificultad']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del ejercicio'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción (opcional)'}),
            'duracion_min': forms.NumberInput(attrs={'placeholder': 'Duración en minutos'}),
            'dificultad': forms.Select(),
        }

class SessionForm(forms.ModelForm):
    """Formulario CRUD para agendamiento de Sesiones."""
    class Meta:
        model = Session
        fields = ['entrenador', 'cliente', 'rutina', 'fecha_hora', 'estado']
        widgets = {
            'entrenador': forms.Select(),
            'cliente': forms.Select(),
            'rutina': forms.Select(),
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estado': forms.Select(),
        }

class ClientExerciseLogForm(forms.ModelForm):
    """Formulario para registro personal de ejercicios por parte del cliente."""
    class Meta:
        model = ClientExerciseLog
        fields = ['ejercicio', 'fecha', 'repeticiones', 'peso']
        widgets = {
            'ejercicio': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'repeticiones': forms.NumberInput(attrs={'min': 1}),
            'peso': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Opcional (kg)'}),
        }
