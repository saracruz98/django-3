from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    """
    Modelo de Usuario Personalizado (CustomUser).
    Hereda de AbstractUser de Django para extender la funcionalidad base, 
    incorporando roles de acceso y validaciones de seguridad de nivel de base de datos.
    
    Implementa la Capa 4 de Seguridad: Restricción de base de datos mediante Regex.
    """

    # Validación Regex (Capa de Seguridad Base de Datos)
    # Impide que se inserten datos maliciosos o formatos incorrectos directamente en BD.
    telefono_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="El número de teléfono debe tener el formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    
    telefono = models.CharField(
        validators=[telefono_regex], 
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Número de contacto validado por Expresión Regular."
    )
    
    # Definición de Roles para Control de Acceso (RBAC)
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('staff', 'Personal'),
        ('customer', 'Cliente'),
    ]
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    # Relación Recursiva: Un usuario (cliente) puede tener asignado a otro usuario (staff).
    entrenador_asignado = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'rol': 'staff'},
        related_name='clientes_asignados',
        help_text="Permite enlazar un cliente directamente con un entrenador de la base de datos."
    )

    def __str__(self):
        """Representación en cadena del usuario (Muestra el username y el nombre completo)."""
        return f"{self.username} ({self.get_full_name()})"
