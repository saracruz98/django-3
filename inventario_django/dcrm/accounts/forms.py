from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    """Formulario de registro de usuarios usando el modelo CustomUser."""

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2", "telefono", "rol")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "rol": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "username": "Usuario",
            "email": "Correo electrónico",
            "telefono": "Teléfono",
            "rol": "Rol",
        }
        help_texts = {
            "username": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono debe contener solo números.')
        if len(telefono) < 7:
            raise forms.ValidationError('El teléfono es demasiado corto.')
        return telefono
