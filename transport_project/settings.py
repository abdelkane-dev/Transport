"""
Configuration principale du projet Django - Transport Réservation.
Auteur : Lead Développeur Backend
"""

import os
from pathlib import Path

# ============================================================
# CHEMINS DE BASE
# ============================================================
# Répertoire racine du projet (là où se trouve manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SÉCURITÉ
# ============================================================
# Clé secrète Django – NE JAMAIS la mettre en production telle quelle
# En production, utilisez une variable d'environnement
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-transport-secret-key-changez-en-production-2024'
)

# Mode debug – mettre à False en production
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Hôtes autorisés – en production, listez vos domaines
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ============================================================
# APPLICATIONS INSTALLÉES
# ============================================================
INSTALLED_APPS = [
    # Applications Django par défaut
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications tierces
    'rest_framework',           # Django REST Framework pour les API
    'rest_framework.authtoken', # Authentification par token DRF

    # Nos applications métier
    'apps.accounts',            # Gestion des comptes utilisateurs
    'apps.bus',                 # Gestion de la flotte de bus
    'apps.trajets',             # Gestion des trajets
    'apps.reservations',        # Gestion des réservations
]

# ============================================================
# MIDDLEWARE
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================
# URLS ET WSGI
# ============================================================
ROOT_URLCONF = 'transport_project.urls'
WSGI_APPLICATION = 'transport_project.wsgi.application'

# ============================================================
# CONFIGURATION DES TEMPLATES
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Répertoire global des templates à la racine du projet
        'DIRS': [BASE_DIR / 'templates'],
        # Chercher aussi dans les répertoires templates/ de chaque app
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                # Nécessaire pour afficher les messages flash (succès, erreurs)
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ============================================================
# BASE DE DONNÉES
# ============================================================
# SQLite par défaut – simple à utiliser, idéal pour le développement
# Pour changer vers PostgreSQL/MySQL, modifiez ce bloc et le .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================================
# VALIDATION DES MOTS DE PASSE
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================
# MODÈLE UTILISATEUR PERSONNALISÉ
# ============================================================
# Indique à Django d'utiliser notre modèle User personnalisé
# IMPORTANT : doit être défini AVANT la première migration
AUTH_USER_MODEL = 'accounts.User'

# ============================================================
# INTERNATIONALISATION
# ============================================================
LANGUAGE_CODE = 'fr-fr'           # Interface en français
TIME_ZONE = 'Africa/Dakar'        # Fuseau horaire Sénégal (UTC+0)
USE_I18N = True                   # Internationalisation activée
USE_TZ = True                     # Support des fuseaux horaires

# ============================================================
# FICHIERS STATIQUES (CSS, JS, images)
# ============================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Dossier statique du développement
STATIC_ROOT = BASE_DIR / 'staticfiles'   # Dossier de collecte pour la production

# ============================================================
# CLÉ PRIMAIRE PAR DÉFAUT
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# AUTHENTIFICATION – REDIRECTION
# ============================================================
LOGIN_URL = '/accounts/connexion/'              # Rediriger si non connecté
LOGIN_REDIRECT_URL = '/reservations/dashboard/' # Après connexion réussie
LOGOUT_REDIRECT_URL = '/'                       # Après déconnexion

# ============================================================
# DJANGO REST FRAMEWORK (DRF)
# ============================================================
REST_FRAMEWORK = {
    # Authentification : session (navigateur) + token (API clients mobiles/JS)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    # Permissions : connecté par défaut pour les API
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    # Format de réponse par défaut
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Interface web DRF
    ],
    # Pagination optionnelle
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ============================================================
# MESSAGES FLASH (notifications utilisateur)
# ============================================================
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',  # Classe Bootstrap 'danger' pour les erreurs
}

# ============================================================
# SESSIONS
# ============================================================
SESSION_COOKIE_AGE = 86400  # Session valide 24 heures (en secondes)
SESSION_SAVE_EVERY_REQUEST = True  # Renouveler la session à chaque requête
