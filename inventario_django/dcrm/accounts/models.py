from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
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
