from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    # Validacion Regex Capa 3: Backend Model Validation para teléfono
    telefono_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="El número de teléfono debe tener el formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    telefono = models.CharField(validators=[telefono_regex], max_length=20, blank=True, null=True)
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('staff', 'Personal'),
        ('customer', 'Cliente'),
    ]
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    entrenador_asignado = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'rol': 'staff'},
        related_name='clientes_asignados',
        help_text="Solo aplicable a clientes."
    )

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
