# Django 3 – Rutinas de Ejercicio

## Descripción
Este proyecto es una aplicación web **Django 5** que gestiona rutinas de ejercicio y permite a los usuarios (ADMIN, STAFF, CUSTOMER) autenticarse con control de acceso basado en roles.  Incluye CRUD completo, un menú **SPA** sin recargas, notificaciones visuales y uso de **Bootstrap 5** local.

## Tecnologías
- **Python 3.14**
- **Django 5.0.14**
- **MySQL / MariaDB 10.6+** (backend de base de datos)
- **Bootstrap 5** (instalado localmente, sin CDN)
- **HTML5, CSS3, JavaScript (ES6)**

## Instalación
```bash
# Clonar el repositorio
git clone https://github.com/saracruz98/django-3.git
cd django-3

# Entorno virtual
python -m venv env
env\Scripts\activate   # Windows

# Dependencias
pip install -r requirements.txt

# Configurar la base de datos (MySQL/MariaDB)
# Editar `dcrm/settings.py` con tus credenciales y ejecutar:
python manage.py migrate

# Ejecutar el servidor de desarrollo
python manage.py runserver
```

## Uso
- Acceder a `http://127.0.0.1:8000/`.
- Registrarse / iniciar sesión → el dashboard se ajusta al rol del usuario.
- Desde el menú SPA se pueden crear, editar y eliminar **rutinas** y **ejercicios**.
- Las alertas aparecen como *toasts* de Bootstrap para confirmar acciones.

## Arquitectura y Modelado
- **UML**: diagramas de clases y secuencia se encuentran en `docs/uml/` (PlantUML).
- **Patrones de diseño**:
  - *Factory Method* (creación de formularios ModelForm)
  - *Strategy* (gestión de roles y permisos)
  - *Template Method* (vistas genéricas para CRUD)
  - *MVC* (estructura clásica de Django)

## Buenas prácticas de seguridad
- Validaciones con expresiones regulares en formularios.
- Uso de `django.contrib.auth` y sesiones firmadas.
- Configuración de cabeceras de seguridad en `settings.py` (CSRF, HSTS, X‑Content‑Type‑Options).

## Contribuir
1. Fork del repositorio.
2. Crear una rama `feature/<nombre>`.
3. Realizar cambios y **commitear cada paso** (objetivo ≥ 20 commits).
4. Abrir Pull Request describiendo los cambios.

## Licencia
Este proyecto está licenciado bajo la **MIT License**.
