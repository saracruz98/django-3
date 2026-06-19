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
