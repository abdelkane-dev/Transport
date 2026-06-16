"""
URLs de l'application Trajets (interface web HTML).
Préfixe : /trajets/
"""

from django.urls import path
from . import views

app_name = 'trajets'

urlpatterns = [
    # Liste des trajets disponibles (accès public)
    path('', views.TrajetListeView.as_view(), name='liste'),
    # Tous les trajets (admin uniquement)
    path('tous/', views.TrajetTousView.as_view(), name='tous'),
    # Détail d'un trajet
    path('<int:pk>/', views.TrajetDetailView.as_view(), name='detail'),
    # Créer un trajet (admin)
    path('creer/', views.TrajetCreerView.as_view(), name='creer'),
    # Modifier un trajet (admin)
    path('<int:pk>/modifier/', views.TrajetModifierView.as_view(), name='modifier'),
    # Supprimer un trajet (admin)
    path('<int:pk>/supprimer/', views.TrajetSupprimerView.as_view(), name='supprimer'),
]
