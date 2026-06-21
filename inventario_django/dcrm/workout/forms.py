from django import forms
from django.contrib.auth import get_user_model
from workout.models import Observation, Progress, Routine, Exercise, Session

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['session', 'texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe la observación aquí...'}),
        }

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['peso', 'altura']
        widgets = {
            'peso': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Peso en kg'}),
            'altura': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Altura en cm'}),
        }

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la rutina'}),
        }

class AssignRoutineForm(forms.Form):
    rutina = forms.ModelChoiceField(queryset=Routine.objects.all(), label='Rutina')
    cliente = forms.ModelChoiceField(queryset=get_user_model().objects.filter(rol='customer'), label='Cliente')

# New forms
class ExerciseForm(forms.ModelForm):
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
