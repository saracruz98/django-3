# 🏋️ Django 5 – Sistema de Gestión de Rutinas de Ejercicio

## 📌 Descripción del proyecto

Este proyecto es una aplicación web desarrollada en Django 5 para la gestión integral de rutinas de ejercicio y control de usuarios en un entorno tipo gimnasio o sistema de entrenamiento. Permite la administración de usuarios con roles (ADMIN, STAFF y CUSTOMER), garantizando control de acceso y seguridad. Incluye funcionalidades CRUD completas para rutinas y ejercicios, con una interfaz dinámica tipo SPA (sin recarga completa de página) usando JavaScript y Bootstrap 5. El sistema sigue la arquitectura MVT (Model–View–Template) de Django y aplica patrones de diseño para mejorar la organización del código y la escalabilidad.

---

## 🎯 Objetivos del sistema

El sistema tiene como objetivo gestionar usuarios, rutinas y ejercicios de manera eficiente, implementando autenticación segura, control de acceso por roles, administración de datos de entrenamiento, interfaz amigable y buenas prácticas de desarrollo web con Django.

---

## 🧰 Tecnologías utilizadas

Python 3.12+, Django 5.0.14, MySQL/MariaDB 10.6+, Bootstrap 5 (local sin CDN), HTML5, CSS3, JavaScript (ES6) y Django ORM para manejo de base de datos.

---

## ⚙️ Instalación y configuración

Primero clona el repositorio con git clone https://github.com/saracruz98/django-3.git y entra al proyecto con cd django-3. Luego crea el entorno virtual con python -m venv env. Actívalo en Windows con env\Scripts\activate o en Linux/Mac con source env/bin/activate. Instala dependencias con pip install -r requirements.txt. Configura la base de datos editando dcrm/settings.py con credenciales MySQL/MariaDB. Ejecuta migraciones con python manage.py makemigrations y python manage.py migrate. Crea un superusuario con python manage.py createsuperuser. Finalmente ejecuta el servidor con python manage.py runserver.

---

## 🚀 Uso del sistema

Abre en el navegador http://127.0.0.1:8000/. Regístrate o inicia sesión. El sistema adapta el dashboard según el rol del usuario (ADMIN, STAFF o CUSTOMER). Desde el panel se pueden crear, editar y eliminar rutinas y ejercicios, además de visualizar información de entrenamiento. El sistema incluye notificaciones tipo Bootstrap Toast para confirmar acciones.

---

## 🏗️ Arquitectura del sistema

El proyecto sigue el patrón MVT (Model–View–Template) de Django. Model se encarga de la base de datos mediante el ORM, View gestiona la lógica del negocio y Template maneja la interfaz de usuario con HTML y Bootstrap. También se aplican patrones de diseño como Factory Method para formularios ModelForm, Strategy para control de roles y permisos, Template Method para vistas basadas en clases (CRUD), y la arquitectura MVC/MVT como base del framework Django.

---

## 🧪 Funcionalidades principales

Incluye registro e inicio de sesión de usuarios, gestión de rutinas, gestión de ejercicios, asignación de rutinas, panel administrativo, control de acceso por roles, validación de formularios, y visualización dinámica de información del usuario.

---

## 🔐 Seguridad del sistema

El sistema implementa autenticación con django.contrib.auth, hash de contraseñas, protección CSRF en formularios, manejo seguro de sesiones, validación de datos en backend y cabeceras de seguridad como HSTS, X-Frame-Options y X-Content-Type-Options para proteger la aplicación.

---

## 📁 Estructura del proyecto

El proyecto está organizado en carpetas principales: dcrm (configuración del proyecto Django), workout (app principal), templates (archivos HTML), static (archivos CSS, JS y Bootstrap local), docs/uml (diagramas UML en PlantUML), manage.py como archivo principal de ejecución y base de datos.

---

## 📊 UML del sistema

Los diagramas UML incluyen diagrama de clases, diagrama de secuencia y casos de uso. Se encuentran ubicados en docs/uml/.

---

## 🤝 Contribución

Para contribuir al proyecto realiza un fork del repositorio, crea una rama con git checkout -b feature/nueva-funcionalidad, realiza cambios con commits frecuentes, y abre un Pull Request explicando claramente los cambios realizados.

---

## 📌 Buenas prácticas

El proyecto sigue buenas prácticas como código modular, separación de responsabilidades MVT, uso del ORM en lugar de SQL directo, validación de datos en backend, reutilización de componentes y diseño responsive con Bootstrap.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT, lo que permite su uso, modificación y distribución libremente, siempre respetando la autoría original del proyecto.

---

## 👨‍💻 Autor

Desarrollado por Sara Villada como proyecto académico de desarrollo web con Django, enfocado en la gestión de rutinas de ejercicio, control de usuarios y aplicación de buenas prácticas de programación.
