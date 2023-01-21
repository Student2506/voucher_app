"""General app module."""

from django.apps import AppConfig


class VistaModuleConfig(AppConfig):
    """Vista module app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vista_module'
