"""
Módulo de formularios para la aplicación website.
Contiene los formularios personalizados utilizados, como el formulario de registro.
"""
from django import forms
from django.contrib.auth import get_user_model


class SignUpForm(forms.ModelForm):
    """
    Formulario personalizado para el registro de nuevos usuarios.
    Hereda de ModelForm y utiliza el modelo User integrado de Django.
    """
    # Campo de contraseña con widget PasswordInput para ocultar los caracteres
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Contraseña",
    )
    # El email es opcional en el modelo User por defecto; lo hacemos requerido aquí
    email = forms.EmailField(
        required=True,
        label="Correo Electrónico",
    )

    class Meta:
        model = get_user_model()
        # Campos que se mostrarán y guardarán en el formulario
        fields = ("username", "email", "password")

    def clean_email(self):
        """Valida que el correo electrónico no esté ya registrado."""
        email = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def save(self, commit=True):
        """
        Sobrescribe el método save() para hashear la contraseña antes de guardar.

        Args:
            commit (bool): Si es True, guarda el objeto en la base de datos inmediatamente.

        Returns:
            User: La instancia del usuario recién creado.
        """
        user = super().save(commit=False)
        # Se hashea la contraseña usando el sistema de seguridad de Django
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
