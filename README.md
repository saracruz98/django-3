# 🏋️ Django 5 – Sistema de Rutinas de Ejercicio

## 📌 Descripción

Este proyecto es una aplicación web desarrollada con **Django 5** para la gestión de rutinas de ejercicio.

Permite la autenticación de usuarios con control de acceso basado en roles (**ADMIN, STAFF y CUSTOMER**), ofreciendo funcionalidades completas de CRUD para rutinas y ejercicios.

La interfaz cuenta con navegación dinámica tipo SPA (sin recarga completa de página), notificaciones visuales mediante **Bootstrap 5**, y una arquitectura basada en el patrón **MVT (Model–View–Template)** de Django.

---

## 🧰 Tecnologías

- Python 3.12+
- Django 5.0.14
- MySQL / MariaDB 10.6+
- Bootstrap 5 (local, sin CDN)
- HTML5
- CSS3
- JavaScript (ES6)

---

## ⚙️ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/saracruz98/django-3.git
cd django-3

# Crear entorno virtual
python -m venv env

# Activar entorno (Windows)
env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos (MySQL/MariaDB)
# Editar dcrm/settings.py con credenciales

# Ejecutar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver
