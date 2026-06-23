import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from workout.models import Exercise

def seed():
    exercises = [
        # Pecho
        ("Press de Banca Plano", "Ejercicio compuesto para pecho", 45, "media"),
        ("Press de Banca Inclinado", "Enfoque en pecho superior", 45, "media"),
        ("Aperturas con Mancuernas", "Aislamiento de pecho", 30, "baja"),
        ("Cruces en Polea", "Aislamiento de pecho en poleas", 30, "baja"),
        ("Flexiones de Pecho (Push-ups)", "Ejercicio corporal para pecho", 20, "baja"),
        ("Pullover con Mancuerna", "Trabajo de pecho y dorsal", 30, "media"),
        ("Press Declinado", "Enfoque en pecho inferior", 45, "alta"),
        ("Peck Deck (Máquina)", "Aislamiento en máquina", 30, "baja"),

        # Espalda
        ("Dominadas (Pull-ups)", "Ejercicio corporal para espalda", 30, "alta"),
        ("Remo con Barra", "Ejercicio compuesto para espalda", 45, "alta"),
        ("Jalón al Pecho", "Trabajo en polea para dorsales", 30, "media"),
        ("Remo Gironda", "Remo sentado en polea baja", 30, "media"),
        ("Remo con Mancuerna a 1 Mano", "Trabajo unilateral de espalda", 35, "media"),
        ("Peso Muerto", "Ejercicio compuesto cuerpo completo", 60, "alta"),
        ("Hiperextensiones", "Fortalecimiento de zona lumbar", 20, "baja"),
        ("Face Pull", "Trabajo de deltoides posterior", 20, "baja"),

        # Piernas (Cuádriceps, Femorales, Glúteos, Gemelos)
        ("Sentadilla Libre", "Ejercicio compuesto principal de pierna", 60, "alta"),
        ("Prensa de Piernas", "Trabajo de pierna en máquina", 45, "media"),
        ("Extensiones de Cuádriceps", "Aislamiento de cuádriceps", 30, "baja"),
        ("Curl Femoral Tumbado", "Aislamiento de isquiotibiales", 30, "baja"),
        ("Peso Muerto Rumano", "Enfoque en isquios y glúteos", 45, "alta"),
        ("Zancadas (Lunges)", "Trabajo unilateral de pierna", 40, "media"),
        ("Hip Thrust", "Ejercicio principal para glúteos", 45, "alta"),
        ("Elevación de Talones de Pie", "Trabajo de gemelos", 20, "baja"),
        ("Elevación de Talones Sentado", "Trabajo de soleo", 20, "baja"),
        ("Sentadilla Búlgara", "Zancada con pie elevado", 40, "alta"),
        ("Máquina Abductora", "Trabajo de abductores", 20, "baja"),
        ("Máquina Adductora", "Trabajo de adductores", 20, "baja"),

        # Hombros
        ("Press Militar con Barra", "Ejercicio principal de hombro", 45, "alta"),
        ("Press Arnold", "Variación de press con mancuernas", 35, "media"),
        ("Elevaciones Laterales", "Aislamiento de deltoides lateral", 30, "baja"),
        ("Elevaciones Frontales", "Aislamiento de deltoides frontal", 20, "baja"),
        ("Pájaros (Elevaciones Posteriores)", "Deltoides posterior", 30, "media"),
        ("Encogimientos (Shrugs)", "Trabajo de trapecio", 20, "baja"),

        # Brazos (Bíceps y Tríceps)
        ("Curl con Barra (Bíceps)", "Ejercicio principal de bíceps", 30, "media"),
        ("Curl Martillo", "Enfoque en braquial", 30, "baja"),
        ("Curl Alterno con Mancuernas", "Trabajo unilateral de bíceps", 30, "baja"),
        ("Curl en Banco Scott", "Aislamiento estricto de bíceps", 30, "media"),
        ("Fondos en Paralelas (Dips)", "Ejercicio compuesto tríceps/pecho", 30, "alta"),
        ("Press Francés", "Aislamiento de tríceps", 35, "media"),
        ("Extensión de Tríceps en Polea", "Aislamiento con cuerda/barra", 25, "baja"),
        ("Patada de Tríceps", "Trabajo con mancuerna para tríceps", 20, "baja"),

        # Abdomen / Core
        ("Crunch Abdominal", "Ejercicio básico de abdomen", 15, "baja"),
        ("Plancha (Plank)", "Trabajo isométrico de core", 15, "media"),
        ("Elevación de Piernas Colgado", "Abdomen inferior", 25, "alta"),
        ("Rueda Abdominal (Ab Wheel)", "Trabajo avanzado de core", 20, "alta"),
        ("Giros Rusos (Russian Twists)", "Trabajo de oblicuos", 15, "baja"),

        # Cardio / Acondicionamiento
        ("Cinta de Correr", "Cardio continuo", 30, "baja"),
        ("Bicicleta Estática", "Cardio de bajo impacto", 30, "baja"),
        ("Elíptica", "Cardio cuerpo completo", 30, "baja"),
    ]

    count = 0
    for nombre, desc, dur, dif in exercises:
        obj, created = Exercise.objects.get_or_create(
            nombre=nombre,
            defaults={
                'descripcion': desc,
                'duracion_min': dur,
                'dificultad': dif
            }
        )
        if created:
            count += 1
    
    print(f"Se crearon {count} ejercicios nuevos. (Total de {len(exercises)} intentados)")

if __name__ == '__main__':
    seed()
