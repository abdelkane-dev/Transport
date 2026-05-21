"""
URLs de l'API REST pour l'application Comptes.
Préfixe : /api/accounts/
"""

from django.urls import path
from . import views

app_name = 'api-accounts'

urlpatterns = [
    # POST : créer un compte
    path('inscription/', views.APIInscriptionView.as_view(), name='api-inscription'),
    # POST : se connecter et obtenir un token
    path('connexion/', views.APIConnexionView.as_view(), name='api-connexion'),
    # POST : se déconnecter (supprimer le token)
    path('deconnexion/', views.APIDeconnexionView.as_view(), name='api-deconnexion'),
    # GET/PUT : voir et modifier son profil
    path('profil/', views.APIProfilView.as_view(), name='api-profil'),
]
