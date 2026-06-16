#!/usr/bin/env python
"""
Point d'entrée Django pour la gestion du projet en ligne de commande.
Utilisation : python manage.py <commande>
"""
import os
import sys


def main():
    """Lance les tâches administratives Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Vérifiez que Django est installé "
            "et disponible dans votre environnement virtuel."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
