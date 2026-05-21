"""
Configuration WSGI pour le projet Transport Réservation.
Utilisé par les serveurs de production (Gunicorn, uWSGI, etc.).
"""

import os
from django.core.wsgi import get_wsgi_application

# Définir le module de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_project.settings')

# Créer l'application WSGI
application = get_wsgi_application()
