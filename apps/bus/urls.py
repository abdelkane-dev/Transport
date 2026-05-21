"""
URLs de l'application Bus (interface web HTML).
Préfixe : /bus/
"""

from django.urls import path
from . import views

app_name = 'bus'

urlpatterns = [
    # Liste de tous les bus
    path('', views.BusListeView.as_view(), name='liste'),
    # Détail d'un bus
    path('<int:pk>/', views.BusDetailView.as_view(), name='detail'),
    # Créer un nouveau bus (admin uniquement)
    path('creer/', views.BusCreerView.as_view(), name='creer'),
    # Modifier un bus (admin uniquement)
    path('<int:pk>/modifier/', views.BusModifierView.as_view(), name='modifier'),
    # Supprimer un bus (admin uniquement)
    path('<int:pk>/supprimer/', views.BusSupprimerView.as_view(), name='supprimer'),
]
