"""
Vues de l'application Réservations.
Gère : dashboard client, création, annulation, liste des réservations.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden

# Importations DRF
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Reservation
from .forms import ReservationForm, AnnulationForm
from .serializers import ReservationSerializer
from apps.trajets.models import Trajet


# ============================================================
# VUES HTML (interface web)
# ============================================================

class DashboardView(LoginRequiredMixin, ListView):
    """
    Dashboard du client : affiche toutes ses réservations.
    Accessible uniquement aux utilisateurs connectés.
    GET /reservations/dashboard/
    """
    model = Reservation
    template_name = 'reservations/dashboard.html'
    context_object_name = 'reservations'
    login_url = '/accounts/connexion/'
    paginate_by = 10

    def get_queryset(self):
        """
        IMPORTANT : chaque client ne voit QUE ses propres réservations.
        Filtrées par l'utilisateur connecté (request.user).
        """
        return Reservation.objects.filter(
            client=self.request.user
        ).select_related('trajet', 'trajet__bus').order_by('-date_reservation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Statistiques pour le dashboard
        reservations = Reservation.objects.filter(client=user)
        context['total_reservations'] = reservations.count()
        context['reservations_actives'] = reservations.filter(
            statut__in=['EN_ATTENTE', 'CONFIRMEE']
        ).count()
        context['reservations_annulees'] = reservations.filter(statut='ANNULEE').count()
        return context


class ReservationDetailView(LoginRequiredMixin, DetailView):
    """
    Détail d'une réservation.
    IMPORTANT : vérifie que la réservation appartient au client connecté.
    GET /reservations/<id>/
    """
    model = Reservation
    template_name = 'reservations/reservation_detail.html'
    context_object_name = 'reservation'
    login_url = '/accounts/connexion/'

    def get_object(self, queryset=None):
        """Récupère la réservation ET vérifie qu'elle appartient au client."""
        reservation = get_object_or_404(Reservation, pk=self.kwargs['pk'])
        # Seul le propriétaire ou un admin peut voir cette réservation
        if reservation.client != self.request.user and not self.request.user.is_staff:
            return None
        return reservation

    def get(self, request, *args, **kwargs):
        """Rediriger si l'objet est None (accès non autorisé)."""
        self.object = self.get_object()
        if self.object is None:
            messages.error(request, "Accès non autorisé à cette réservation.")
            return redirect('reservations:dashboard')
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['peut_annuler'] = self.object.peut_etre_annulee()
            context['prix_total'] = self.object.get_prix_total()
        return context


class ReservationCreerView(LoginRequiredMixin, View):
    """
    Vue de création d'une réservation.
    POST depuis la page de détail d'un trajet.
    GET  /reservations/creer/<trajet_id>/  → formulaire de réservation
    POST /reservations/creer/<trajet_id>/  → soumettre la réservation
    """
    template_name = 'reservations/reservation_creer.html'
    login_url = '/accounts/connexion/'

    def get(self, request, trajet_id):
        """Affiche le formulaire de réservation pour un trajet donné."""
        trajet = get_object_or_404(Trajet, pk=trajet_id)

        # Vérifications préalables
        if trajet.est_passe():
            messages.error(request, "Ce trajet est déjà passé. Impossible de réserver.")
            return redirect('trajets:liste')

        if trajet.est_complet():
            messages.error(request, "Ce trajet est complet. Aucune place disponible.")
            return redirect('trajets:detail', pk=trajet_id)

        form = ReservationForm(trajet=trajet)
        return render(request, self.template_name, {
            'form': form,
            'trajet': trajet,
            'places_disponibles': trajet.get_places_disponibles(),
        })

    def post(self, request, trajet_id):
        """Traite la soumission du formulaire de réservation."""
        trajet = get_object_or_404(Trajet, pk=trajet_id)
        form = ReservationForm(request.POST, trajet=trajet)

        if form.is_valid():
            # Créer la réservation sans sauvegarder (commit=False)
            reservation = form.save(commit=False)
            reservation.client = request.user  # Assigner le client connecté
            reservation.trajet = trajet

            try:
                # Valider les règles métier du modèle
                reservation.full_clean()
                reservation.save()
                messages.success(
                    request,
                    f"Réservation effectuée avec succès ! "
                    f"{reservation.nombre_places} place(s) réservée(s) sur le trajet "
                    f"{trajet.ville_depart} → {trajet.ville_arrivee}."
                )
                return redirect('reservations:detail', pk=reservation.pk)
            except Exception as e:
                messages.error(request, f"Erreur lors de la réservation : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

        return render(request, self.template_name, {
            'form': form,
            'trajet': trajet,
            'places_disponibles': trajet.get_places_disponibles(),
        })


class ReservationAnnulerView(LoginRequiredMixin, View):
    """
    Vue d'annulation d'une réservation.
    GET  /reservations/<id>/annuler/ → page de confirmation
    POST /reservations/<id>/annuler/ → annuler
    """
    template_name = 'reservations/reservation_annuler.html'
    login_url = '/accounts/connexion/'

    def get_reservation_or_403(self, request, pk):
        """Récupère la réservation et vérifie les droits d'accès."""
        reservation = get_object_or_404(Reservation, pk=pk)
        if reservation.client != request.user and not request.user.is_staff:
            messages.error(request, "Vous ne pouvez annuler que vos propres réservations.")
            return None
        return reservation

    def get(self, request, pk):
        """Affiche la page de confirmation d'annulation."""
        reservation = self.get_reservation_or_403(request, pk)
        if reservation is None:
            return redirect('reservations:dashboard')

        if not reservation.peut_etre_annulee():
            messages.warning(
                request,
                "Cette réservation ne peut pas être annulée "
                "(déjà annulée ou trajet passé)."
            )
            return redirect('reservations:detail', pk=pk)

        form = AnnulationForm()
        return render(request, self.template_name, {
            'reservation': reservation,
            'form': form,
        })

    def post(self, request, pk):
        """Traite l'annulation de la réservation."""
        reservation = self.get_reservation_or_403(request, pk)
        if reservation is None:
            return redirect('reservations:dashboard')

        form = AnnulationForm(request.POST)
        if form.is_valid():
            raison = form.cleaned_data.get('raison', '')
            succes, message = reservation.annuler(raison=raison)

            if succes:
                messages.success(request, message)
                return redirect('reservations:dashboard')
            else:
                messages.error(request, message)

        return render(request, self.template_name, {
            'reservation': reservation,
            'form': form,
        })


@login_required(login_url='/accounts/connexion/')
def admin_reservations_view(request):
    """
    Vue admin : liste de TOUTES les réservations.
    Réservée aux administrateurs (is_staff).
    GET /reservations/admin/
    """
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('reservations:dashboard')

    reservations = Reservation.objects.select_related(
        'client', 'trajet', 'trajet__bus'
    ).all()

    # Filtres
    statut = request.GET.get('statut', '')
    if statut:
        reservations = reservations.filter(statut=statut)

    return render(request, 'reservations/admin_reservations.html', {
        'reservations': reservations,
        'statut_filtre': statut,
        'total': reservations.count(),
    })


@login_required(login_url='/accounts/connexion/')
def confirmer_reservation_view(request, pk):
    """
    Vue admin : confirmer une réservation EN_ATTENTE.
    POST /reservations/<id>/confirmer/
    """
    if not request.user.is_staff:
        messages.error(request, "Action réservée aux administrateurs.")
        return redirect('reservations:dashboard')

    reservation = get_object_or_404(Reservation, pk=pk)
    succes, message = reservation.confirmer()

    if succes:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect('reservations:admin')


# ============================================================
# VUES API REST (DRF)
# ============================================================

class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF pour les réservations.
    Un client ne voit/modifie que SES réservations.
    Un admin voit toutes les réservations.

    GET    /api/reservations/           → mes réservations
    POST   /api/reservations/           → créer une réservation
    GET    /api/reservations/<id>/      → détail
    DELETE /api/reservations/<id>/      → annuler
    POST   /api/reservations/<id>/annuler/ → annuler avec raison
    """
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtre strictement par utilisateur connecté.
        Les admins voient toutes les réservations.
        """
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.select_related(
                'client', 'trajet', 'trajet__bus'
            ).all()
        # Clients normaux : seulement leurs réservations
        return Reservation.objects.filter(client=user).select_related(
            'trajet', 'trajet__bus'
        )

    def perform_create(self, serializer):
        """Assigner automatiquement le client connecté lors de la création."""
        serializer.save(client=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Annule la réservation au lieu de la supprimer.
        Empêche la suppression si le trajet est passé.
        """
        reservation = self.get_object()
        succes, message = reservation.annuler()
        if succes:
            return Response({'message': message}, status=status.HTTP_200_OK)
        return Response({'erreur': message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='annuler')
    def annuler(self, request, pk=None):
        """
        Action personnalisée pour annuler avec une raison.
        POST /api/reservations/<id>/annuler/
        Corps : { "raison": "..." }
        """
        reservation = self.get_object()
        raison = request.data.get('raison', '')
        succes, message = reservation.annuler(raison=raison)
        if succes:
            return Response({'message': message})
        return Response({'erreur': message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='confirmer')
    def confirmer(self, request, pk=None):
        """
        Action admin : confirmer une réservation.
        POST /api/reservations/<id>/confirmer/
        """
        if not request.user.is_staff:
            return Response(
                {'erreur': 'Action réservée aux administrateurs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        reservation = self.get_object()
        succes, message = reservation.confirmer()
        if succes:
            return Response({'message': message})
        return Response({'erreur': message}, status=status.HTTP_400_BAD_REQUEST)
