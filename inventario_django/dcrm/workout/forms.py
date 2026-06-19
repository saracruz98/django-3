from django import forms
from workout.models import Observation

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['session', 'texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe la observación aquí...'}),
        }
