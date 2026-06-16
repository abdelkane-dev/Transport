"""
Vues de l'application Trajets.
Gère le CRUD des trajets via interface web HTML et API REST.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import date

# Importations DRF
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Trajet
from .forms import TrajetForm, RechercheTrajetForm
from .serializers import TrajetSerializer


# ============================================================
# MIXIN : Restriction aux administrateurs
# ============================================================

class AdminRequiredMixin(UserPassesTestMixin):
    """Restreint l'accès aux administrateurs (is_staff)."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Accès refusé. Action réservée aux administrateurs.")
        return redirect('trajets:liste')


# ============================================================
# VUES HTML (interface web)
# ============================================================

class TrajetListeView(ListView):
    """
    Vue listant les trajets disponibles (à venir, non complets).
    Inclut la recherche par ville et date.
    GET /trajets/
    GET /trajets/?ville_depart=Dakar&ville_arrivee=Thies&date_depart=2024-06-15
    """
    model = Trajet
    template_name = 'trajets/trajet_liste.html'
    context_object_name = 'trajets'
    paginate_by = 10

    def get_queryset(self):
        """
        Filtre les trajets selon les paramètres de recherche GET.
        Par défaut : uniquement les trajets dont la date est aujourd'hui ou future.
        """
        queryset = Trajet.objects.select_related('bus').filter(
            date_depart__gte=date.today()
        )

        # Filtrage par ville de départ
        ville_depart = self.request.GET.get('ville_depart', '').strip()
        if ville_depart:
            queryset = queryset.filter(ville_depart__icontains=ville_depart)

        # Filtrage par ville d'arrivée
        ville_arrivee = self.request.GET.get('ville_arrivee', '').strip()
        if ville_arrivee:
            queryset = queryset.filter(ville_arrivee__icontains=ville_arrivee)

        # Filtrage par date
        date_depart = self.request.GET.get('date_depart', '').strip()
        if date_depart:
            queryset = queryset.filter(date_depart=date_depart)

        return queryset.order_by('date_depart', 'heure_depart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passer le formulaire de recherche avec les valeurs actuelles
        context['form_recherche'] = RechercheTrajetForm(self.request.GET or None)
        context['total_trajets'] = Trajet.objects.filter(
            date_depart__gte=date.today()
        ).count()
        return context


class TrajetTousView(AdminRequiredMixin, ListView):
    """
    Vue listant TOUS les trajets (y compris passés).
    Réservée aux administrateurs.
    GET /trajets/tous/
    """
    model = Trajet
    template_name = 'trajets/trajet_tous.html'
    context_object_name = 'trajets'
    paginate_by = 20

    def get_queryset(self):
        """Filtres avancés pour l'admin."""
        queryset = Trajet.objects.select_related('bus').all()

        ville_depart = self.request.GET.get('ville_depart', '').strip()
        if ville_depart:
            queryset = queryset.filter(ville_depart__icontains=ville_depart)

        ville_arrivee = self.request.GET.get('ville_arrivee', '').strip()
        if ville_arrivee:
            queryset = queryset.filter(ville_arrivee__icontains=ville_arrivee)

        date_depart = self.request.GET.get('date_depart', '').strip()
        if date_depart:
            queryset = queryset.filter(date_depart=date_depart)

        return queryset.order_by('-date_depart', 'heure_depart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_recherche'] = RechercheTrajetForm(self.request.GET or None)
        context['titre'] = "Tous les trajets (admin)"
        return context


class TrajetDetailView(DetailView):
    """
    Vue de détail d'un trajet avec informations de disponibilité.
    GET /trajets/<id>/
    """
    model = Trajet
    template_name = 'trajets/trajet_detail.html'
    context_object_name = 'trajet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trajet = self.object
        context['places_disponibles'] = trajet.get_places_disponibles()
        context['places_reservees'] = trajet.get_places_reservees()
        context['taux_remplissage'] = trajet.get_taux_remplissage()
        context['est_complet'] = trajet.est_complet()
        context['est_passe'] = trajet.est_passe()
        # Vérifier si l'utilisateur a déjà réservé ce trajet
        if self.request.user.is_authenticated:
            context['deja_reserve'] = trajet.reservations.filter(
                client=self.request.user,
                statut__in=['EN_ATTENTE', 'CONFIRMEE']
            ).exists()
        return context


class TrajetCreerView(AdminRequiredMixin, CreateView):
    """
    Vue de création d'un trajet.
    Réservée aux administrateurs.
    GET /trajets/creer/
    POST /trajets/creer/
    """
    model = Trajet
    form_class = TrajetForm
    template_name = 'trajets/trajet_form.html'
    success_url = reverse_lazy('trajets:liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = "Créer un nouveau trajet"
        context['action'] = "Créer"
        return context

    def form_valid(self, form):
        """
        Avant de sauvegarder, appeler full_clean() du modèle
        pour valider la règle métier (bus ACTIF).
        """
        trajet = form.save(commit=False)
        try:
            trajet.full_clean()  # Déclenche clean() du modèle
            trajet.save()
            messages.success(
                self.request,
                f"Trajet '{trajet}' créé avec succès !"
            )
            return redirect(self.success_url)
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création du trajet. Vérifiez les champs.")
        return super().form_invalid(form)


class TrajetModifierView(AdminRequiredMixin, UpdateView):
    """
    Vue de modification d'un trajet.
    GET /trajets/<id>/modifier/
    POST /trajets/<id>/modifier/
    """
    model = Trajet
    form_class = TrajetForm
    template_name = 'trajets/trajet_form.html'
    success_url = reverse_lazy('trajets:liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = f"Modifier le trajet : {self.object}"
        context['action'] = "Enregistrer"
        return context

    def form_valid(self, form):
        trajet = form.save(commit=False)
        try:
            trajet.full_clean()
            trajet.save()
            messages.success(self.request, f"Trajet modifié avec succès !")
            return redirect(self.success_url)
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class TrajetSupprimerView(AdminRequiredMixin, DeleteView):
    """
    Vue de suppression d'un trajet.
    GET /trajets/<id>/supprimer/
    POST /trajets/<id>/supprimer/
    """
    model = Trajet
    template_name = 'trajets/trajet_supprimer.html'
    success_url = reverse_lazy('trajets:liste')
    context_object_name = 'trajet'

    def form_valid(self, form):
        trajet = self.get_object()
        # Vérifier s'il y a des réservations actives
        reservations_actives = trajet.reservations.filter(
            statut__in=['EN_ATTENTE', 'CONFIRMEE']
        ).count()
        if reservations_actives > 0:
            messages.error(
                self.request,
                f"Impossible de supprimer ce trajet : {reservations_actives} réservation(s) active(s) existent. "
                "Annulez d'abord les réservations."
            )
            return redirect('trajets:detail', pk=trajet.pk)

        nom_trajet = str(trajet)
        response = super().form_valid(form)
        messages.success(self.request, f"Trajet '{nom_trajet}' supprimé avec succès.")
        return response


# ============================================================
# VUES API REST (DRF – ViewSet)
# ============================================================

class TrajetViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF pour le CRUD des trajets.
    GET    /api/trajets/          → liste des trajets à venir
    POST   /api/trajets/          → créer un trajet (admin)
    GET    /api/trajets/<id>/     → détail d'un trajet
    PUT    /api/trajets/<id>/     → modifier (admin)
    PATCH  /api/trajets/<id>/     → modification partielle (admin)
    DELETE /api/trajets/<id>/     → supprimer (admin)
    GET    /api/trajets/recherche/ → recherche avancée
    """
    queryset = Trajet.objects.select_related('bus').all()
    serializer_class = TrajetSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ville_depart', 'ville_arrivee']
    ordering_fields = ['date_depart', 'heure_depart', 'prix']

    def get_queryset(self):
        """Filtre les trajets par paramètres GET."""
        queryset = super().get_queryset()
        ville_depart = self.request.query_params.get('ville_depart')
        ville_arrivee = self.request.query_params.get('ville_arrivee')
        date_depart = self.request.query_params.get('date_depart')

        if ville_depart:
            queryset = queryset.filter(ville_depart__icontains=ville_depart)
        if ville_arrivee:
            queryset = queryset.filter(ville_arrivee__icontains=ville_arrivee)
        if date_depart:
            queryset = queryset.filter(date_depart=date_depart)

        # Par défaut, retourner seulement les trajets futurs
        if not any([ville_depart, ville_arrivee, date_depart]):
            queryset = queryset.filter(date_depart__gte=date.today())

        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        Retourne uniquement les trajets disponibles (non complets, futurs).
        GET /api/trajets/disponibles/
        """
        trajets = [t for t in self.get_queryset() if not t.est_complet()]
        serializer = self.get_serializer(trajets, many=True)
        return Response({'count': len(trajets), 'trajets': serializer.data})
