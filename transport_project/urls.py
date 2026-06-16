"""
Configuration des URLs principales du projet Transport Réservation.
Chaque app possède son propre fichier urls.py inclus ici.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # -------------------------------------------------------
    # Interface d'administration Django
    # -------------------------------------------------------
    path('admin/', admin.site.urls),

    # -------------------------------------------------------
    # Page d'accueil du site
    # -------------------------------------------------------
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # -------------------------------------------------------
    # URLs de l'application Comptes (authentification)
    # -------------------------------------------------------
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),

    # -------------------------------------------------------
    # URLs de l'application Bus (gestion de la flotte)
    # -------------------------------------------------------
    path('bus/', include('apps.bus.urls', namespace='bus')),

    # -------------------------------------------------------
    # URLs de l'application Trajets
    # -------------------------------------------------------
    path('trajets/', include('apps.trajets.urls', namespace='trajets')),

    # -------------------------------------------------------
    # URLs de l'application Réservations
    # -------------------------------------------------------
    path('reservations/', include('apps.reservations.urls', namespace='reservations')),

    # -------------------------------------------------------
    # API REST (DRF) – préfixe /api/
    # -------------------------------------------------------
    path('api/', include([
        path('bus/', include('apps.bus.api_urls', namespace='api-bus')),
        path('trajets/', include('apps.trajets.api_urls', namespace='api-trajets')),
        path('reservations/', include('apps.reservations.api_urls', namespace='api-reservations')),
        path('accounts/', include('apps.accounts.api_urls', namespace='api-accounts')),
    ])),

    # -------------------------------------------------------
    # Authentification DRF (token)
    # -------------------------------------------------------
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personnalisation de l'interface d'administration
admin.site.site_header = "Transport Réservation – Administration"
admin.site.site_title = "Transport Admin"
admin.site.index_title = "Tableau de bord administrateur"
