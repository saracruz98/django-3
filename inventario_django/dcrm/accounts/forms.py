from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    """
    Formulario de registro de usuarios utilizando el Patrón Factory (ModelForm) y el Principio DRY.
    Delega la creación de campos HTML e inicializa validaciones según la estructura del CustomUser.
    
    Aplica la Capa 3 de Seguridad: Limpieza y validación en el Backend antes de guardar en la DB.
    """

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2", "telefono", "rol")
        # Diccionario de widgets: Inyecta clases de Bootstrap y Expresiones Regulares en HTML (Capa 1).
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control", "pattern": "^[a-zA-Z0-9_]+$", "title": "Solo letras, números y guiones bajos (_)."}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "pattern": "^\+?1?\d{9,15}$", "title": "Formato válido: +999999999 (9 a 15 dígitos)."}),
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
        # Se elimina el texto de ayuda predeterminado de Django para un diseño más limpio
        self.fields['username'].help_text = ''

    def clean_telefono(self):
        """
        Validación personalizada (Backend - Capa 3) para el campo teléfono usando Regex.
        Asegura que no se salten la validación del frontend inyectando datos.
        """
        telefono = self.cleaned_data.get('telefono')
        import re
        if not re.match(r'^\+?1?\d{9,15}$', telefono):
            raise forms.ValidationError('El teléfono debe tener un formato válido (ej. +999999999) y entre 9 y 15 dígitos.')
        return telefono
        
    def clean_username(self):
        """
        Validación de seguridad con Expresiones Regulares (Regex) para el nombre de usuario.
        Rechaza caracteres extraños como <, >, ' y " para evitar inyecciones de código.
        """
        username = self.cleaned_data.get('username')
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('El usuario solo puede contener letras, números y guiones bajos (_). No se permiten caracteres especiales ni espacios.')
        return username
