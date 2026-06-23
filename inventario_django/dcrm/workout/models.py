from django.db import models
from django.conf import settings

"""uno"""

class Exercise(models.Model): 

    DIFICULTAD_CHOICES = [
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
    ]

    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Solo letras, números y espacios.",
    )
    descripcion = models.TextField(blank=True)
    duracion_min = models.PositiveIntegerField(help_text="Duración en minutos")
    dificultad = models.CharField(max_length=5, choices=DIFICULTAD_CHOICES)

    def __str__(self):
        return self.nombre

"""dos"""
class Routine(models.Model):
    """
    Modelo de Dominio: Rutina de Entrenamiento.
    Actúa como una entidad agrupadora que vincula a un Usuario con múltiples Ejercicios.
    
    Relaciones Estructurales:
    - FK (ForeignKey) hacia CustomUser: Relación 1:N donde un usuario puede tener muchas rutinas.
    
    Campos Principales:
    - ``nombre``: Nombre de la rutina.
    - ``usuario``: Referencia directa a la cuenta del usuario/cliente.
    - ``fecha_creacion``: Timestamp automático para auditoría.
    - ``activo``: Bandera lógica de activación (Soft Delete o Archivo).
    """

    nombre = models.CharField(max_length=100, help_text="Nombre descriptivo de la rutina")
    descripcion = models.TextField(blank=True, help_text="Descripción detallada de la rutina")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="routines",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ("nombre", "usuario")
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"


class RoutineExercise(models.Model):
    """
    Modelo Intermedio (Tabla de Unión) para la relación N:M entre Routine y Exercise.
    Permite agregar atributos específicos a la relación, como el orden y número de series.
    
    Estructura de Base de Datos:
    - ``rutina``: FK hacia Routine (Cascade delete).
    - ``ejercicio``: FK hacia Exercise.
    - ``orden``: Posición secuencial del ejercicio dentro de la rutina específica.
    - ``repeticiones``: Cantidad de series/repeticiones indicadas por el entrenador.
    """

    rutina = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        related_name="ejercicios",
    )
    ejercicio = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()
    repeticiones = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("rutina", "orden")
        ordering = ["orden"]

    def __str__(self):
        return f"{self.orden}. {self.ejercicio.nombre}"

# ---------------------------------------------------------------------------
# Reglas de negocio (validaciones) por rol
# ---------------------------------------------------------------------------
# • Cliente (rol 'customer') solo ve sus propias rutinas.
# • Staff (rol 'staff') gestiona todas las rutinas.
# • Administrador (superuser) tiene acceso total.
# • Cada usuario tiene un máximo de 5 rutinas activas simultáneas.
# ---------------------------------------------------------------------------


class Session(models.Model):
    """Sesión de entrenamiento programada entre un entrenador y un cliente.

    - ``entrenador``: usuario con rol 'staff'.
    - ``cliente``: usuario con rol 'customer'.
    - ``rutina``: rutina asignada.
    - ``fecha_hora``: fecha y hora programada.
    - ``estado``: estado de la sesión.
    """
    ENTRENADOR_ROL = "staff"
    CLIENTE_ROL = "customer"

    ESTADO_CHOICES = [
        ("programada", "Programada"),
        ("completada", "Completada"),
        ("cancelada", "Cancelada"),
    ]

    entrenador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions_as_trainer",
        limit_choices_to={"rol": ENTRENADOR_ROL},
    )
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions_as_client",
        limit_choices_to={"rol": CLIENTE_ROL},
    )
    rutina = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="sessions")
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="programada")

    class Meta:
        ordering = ["-fecha_hora"]
        unique_together = ("entrenador", "cliente", "fecha_hora")

    def __str__(self):
        return f"{self.entrenador.username} → {self.cliente.username} @ {self.fecha_hora:%Y-%m-%d %H:%M}"


class Observation(models.Model):
    """Observación escrita por un entrenador durante una sesión.

    - ``session``: sesión a la que pertenece la observación.
    - ``texto``: contenido de la observación.
    - ``creado_por``: usuario que la escribe (el entrenador).
    - ``fecha``: marca temporal automática.
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="observaciones")
    texto = models.TextField()
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="observaciones_creadas")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Obs {self.id} de {self.creado_por.username} @ {self.fecha:%Y-%m-%d %H:%M}"

class Progress(models.Model):
    """Progreso físico del cliente (peso, altura, masa muscular)."""
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"rol": "customer"},
        related_name="progresos",
    )
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kg")
    altura = models.DecimalField(max_digits=4, decimal_places=1, help_text="Altura en cm")
    muscle_mass = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Masa muscular en kg")
    fecha = models.DateField(auto_now_add=True, help_text="Fecha del registro")

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.cliente.username} – {self.fecha}"

class Recommendation(models.Model):
    """Recomendaciones personalizadas para el cliente."""
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"rol": "customer"},
        related_name="recomendaciones",
    )
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Recomendación {self.id} para {self.cliente.username}"

class ClientExerciseLog(models.Model):
    """Registro personal de ejercicios realizados por el cliente."""
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"rol": "customer"},
        related_name="ejercicios_registrados",
    )
    ejercicio = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    fecha = models.DateField(help_text="Fecha en que se realizó el ejercicio")
    repeticiones = models.PositiveIntegerField(default=1, help_text="Cantidad de repeticiones o series")
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Peso utilizado (kg) opcional")
    
    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.cliente.username} - {self.ejercicio.nombre} ({self.fecha})"
