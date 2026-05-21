"""
URLs de l'application Réservations (interface web HTML).
Préfixe : /reservations/
"""

from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    # Dashboard du client (ses réservations)
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # Détail d'une réservation
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='detail'),
    # Créer une réservation pour un trajet
    path('creer/<int:trajet_id>/', views.ReservationCreerView.as_view(), name='creer'),
    # Annuler une réservation
    path('<int:pk>/annuler/', views.ReservationAnnulerView.as_view(), name='annuler'),
    # Vue admin : toutes les réservations
    path('admin/', views.admin_reservations_view, name='admin'),
    # Admin : confirmer une réservation
    path('<int:pk>/confirmer/', views.confirmer_reservation_view, name='confirmer'),
]
