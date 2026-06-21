import os
import django
from django.utils import timezone
from datetime import timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from django.contrib.auth import get_user_model
from workout.models import Exercise, Routine, RoutineExercise, Session, Progress, Observation, Recommendation

User = get_user_model()

def create_mock_data():
    # Obtener un cliente (customer) y un entrenador (staff)
    cliente = User.objects.filter(rol='customer').first()
    entrenador = User.objects.filter(rol='staff').first()
    
    if not cliente or not entrenador:
        print("Faltan usuarios: Asegúrate de tener al menos un usuario 'customer' y un 'staff'.")
        return

    print(f"Generando datos para el cliente: {cliente.username} y entrenador: {entrenador.username}")

    # Limpiar datos previos del cliente para evitar duplicados si se corre múltiples veces
    Routine.objects.filter(usuario=cliente).delete()
    Session.objects.filter(cliente=cliente).delete()
    Progress.objects.filter(cliente=cliente).delete()
    Recommendation.objects.filter(cliente=cliente).delete()

    # --- Crear Ejercicios base ---
    ejercicios_data = [
        ("Press de banca", 15, "media"),
        ("Sentadilla", 20, "alta"),
        ("Peso muerto", 20, "alta"),
        ("Dominadas", 15, "alta"),
        ("Curl de bíceps", 10, "baja")
    ]
    
    ejercicios = []
    for nombre, duracion, diff in ejercicios_data:
        ej, _ = Exercise.objects.get_or_create(
            nombre=nombre, 
            defaults={'duracion_min': duracion, 'dificultad': diff, 'descripcion': f'Ejercicio de {nombre}'}
        )
        ejercicios.append(ej)

    # --- Crear Rutina ---
    rutina = Routine.objects.create(nombre="Fuerza y Volumen - Mes 1", usuario=cliente, activo=True)
    
    for i, ej in enumerate(ejercicios):
        RoutineExercise.objects.create(
            rutina=rutina,
            ejercicio=ej,
            orden=i+1,
            repeticiones=random.randint(3, 5) * 10 # ej. 30, 40, 50 que representen series x reps
        )

    # --- Crear Progreso Físico (Últimos 3 meses) ---
    today = timezone.now()
    for i in range(12, -1, -1):
        fecha_prog = today - timedelta(days=i*7) # Un registro cada semana
        peso_base = 70.0 + random.uniform(-1, 1) + (12 - i) * 0.2  # Va subiendo de peso de a poco
        masa_base = 35.0 + (12 - i) * 0.15 # Va subiendo masa muscular
        
        p = Progress.objects.create(
            cliente=cliente,
            peso=round(peso_base, 2),
            altura=175.0,
            muscle_mass=round(masa_base, 2),
        )
        # Sobrescribimos la fecha ya que auto_now_add la fija a hoy
        Progress.objects.filter(id=p.id).update(fecha=fecha_prog.date())

    # --- Crear Sesiones (Historial y Próxima) ---
    # Historial de las últimas 4 semanas (ej. 3 veces por semana)
    for i in range(28, 0, -1):
        # Entrenando Lunes, Miércoles y Viernes
        fecha_ses = today - timedelta(days=i)
        if fecha_ses.weekday() in [0, 2, 4]: 
            ses = Session.objects.create(
                entrenador=entrenador,
                cliente=cliente,
                rutina=rutina,
                fecha_hora=fecha_ses.replace(hour=18, minute=0),
                estado="completada"
            )
            # Agregar observación a algunas sesiones
            if random.random() > 0.6:
                Observation.objects.create(
                    session=ses,
                    creado_por=entrenador,
                    texto=random.choice([
                        "Buen trabajo hoy, aumentaste peso en sentadilla.",
                        "Recuerda mantener la espalda recta en el peso muerto.",
                        "Excelente energía, logramos completar todas las series."
                    ])
                )

    # Próxima sesión
    proxima_fecha = today + timedelta(days=2)
    Session.objects.create(
        entrenador=entrenador,
        cliente=cliente,
        rutina=rutina,
        fecha_hora=proxima_fecha.replace(hour=18, minute=0),
        estado="programada"
    )

    # --- Crear Recomendaciones ---
    Recommendation.objects.create(
        cliente=cliente,
        texto="No olvides consumir al menos 2 gramos de proteína por kilo de peso corporal."
    )
    Recommendation.objects.create(
        cliente=cliente,
        texto="Trata de dormir al menos 7-8 horas diarias para optimizar la recuperación muscular."
    )

    print("Datos mock generados con éxito!")

if __name__ == '__main__':
    create_mock_data()
