"""Configuration de l'application Bus."""
from django.apps import AppConfig


class BusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bus'
    verbose_name = 'Gestion des Bus'
