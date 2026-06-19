"""
Módulo de configuración de la aplicación website.
Define la clase de configuración principal para esta aplicación Django.
"""
from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """
    Configuración de la aplicación 'website'.
    Define el tipo de campo automático por defecto y el nombre de la aplicación.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'
