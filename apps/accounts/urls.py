"""
URLs de l'application Comptes (interface web HTML).
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Page d'inscription
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),
    # Page de connexion
    path('connexion/', views.ConnexionView.as_view(), name='connexion'),
    # Déconnexion
    path('deconnexion/', views.DeconnexionView.as_view(), name='deconnexion'),
    # Profil utilisateur (protégé par LoginRequiredMixin)
    path('profil/', views.ProfilView.as_view(), name='profil'),
]
