"""
Vues de l'application Bus.
Gère le CRUD des bus via interface web HTML et API REST.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Importations DRF
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bus
from .forms import BusForm
from .serializers import BusSerializer


# ============================================================
# MIXIN : Restriction aux administrateurs
# ============================================================

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin qui restreint l'accès aux administrateurs (is_staff).
    Pour les opérations sensibles comme créer/modifier/supprimer un bus.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Accès refusé. Seuls les administrateurs peuvent effectuer cette action."
        )
        return redirect('bus:liste')


# ============================================================
# VUES HTML (interface web)
# ============================================================

class BusListeView(ListView):
    """
    Vue listant tous les bus de la flotte.
    Accessible à tous (visiteurs et connectés).
    GET /bus/
    """
    model = Bus
    template_name = 'bus/bus_liste.html'
    context_object_name = 'bus_list'
    paginate_by = 10  # 10 bus par page

    def get_queryset(self):
        """Permet de filtrer par statut via le paramètre GET ?statut=ACTIF."""
        queryset = Bus.objects.all()
        statut = self.request.GET.get('statut')
        if statut in ['ACTIF', 'INACTIF', 'MAINTENANCE']:
            queryset = queryset.filter(statut=statut)
        return queryset

    def get_context_data(self, **kwargs):
        """Ajoute le filtre sélectionné au contexte du template."""
        context = super().get_context_data(**kwargs)
        context['statut_filtre'] = self.request.GET.get('statut', '')
        context['total_bus'] = Bus.objects.count()
        context['bus_actifs'] = Bus.objects.filter(statut='ACTIF').count()
        return context


class BusDetailView(DetailView):
    """
    Vue de détail d'un bus.
    GET /bus/<id>/
    """
    model = Bus
    template_name = 'bus/bus_detail.html'
    context_object_name = 'bus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer les trajets liés à ce bus
        context['trajets'] = self.object.trajets.all().order_by('-date_depart')
        return context


class BusCreerView(AdminRequiredMixin, CreateView):
    """
    Vue de création d'un nouveau bus.
    Réservée aux administrateurs (AdminRequiredMixin).
    GET /bus/creer/ → formulaire vide
    POST /bus/creer/ → créer le bus
    """
    model = Bus
    form_class = BusForm
    template_name = 'bus/bus_form.html'
    success_url = reverse_lazy('bus:liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = "Ajouter un nouveau bus"
        context['action'] = "Ajouter"
        return context

    def form_valid(self, form):
        """Appelé quand le formulaire est valide – sauvegarde et message."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Bus '{self.object.immatriculation}' ajouté avec succès !"
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de l'ajout du bus. Vérifiez les champs.")
        return super().form_invalid(form)


class BusModifierView(AdminRequiredMixin, UpdateView):
    """
    Vue de modification d'un bus existant.
    Réservée aux administrateurs.
    GET /bus/<id>/modifier/ → formulaire pré-rempli
    POST /bus/<id>/modifier/ → sauvegarder les modifications
    """
    model = Bus
    form_class = BusForm
    template_name = 'bus/bus_form.html'
    success_url = reverse_lazy('bus:liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titre'] = f"Modifier le bus {self.object.immatriculation}"
        context['action'] = "Enregistrer"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Bus '{self.object.immatriculation}' modifié avec succès !"
        )
        return response


class BusSupprimerView(AdminRequiredMixin, DeleteView):
    """
    Vue de suppression d'un bus.
    Réservée aux administrateurs.
    GET /bus/<id>/supprimer/ → confirmation
    POST /bus/<id>/supprimer/ → supprimer
    """
    model = Bus
    template_name = 'bus/bus_supprimer.html'
    success_url = reverse_lazy('bus:liste')
    context_object_name = 'bus'

    def form_valid(self, form):
        """Vérifie qu'il n'y a pas de trajets liés avant de supprimer."""
        bus = self.get_object()
        if bus.trajets.exists():
            messages.error(
                self.request,
                f"Impossible de supprimer ce bus : il est lié à {bus.get_nombre_trajets()} trajet(s). "
                "Supprimez d'abord les trajets associés."
            )
            return redirect('bus:detail', pk=bus.pk)
        messages.success(
            self.request,
            f"Bus '{bus.immatriculation}' supprimé définitivement."
        )
        return super().form_valid(form)


# ============================================================
# VUES API REST (DRF – ViewSet)
# ============================================================

class BusViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF pour le CRUD complet des bus via API.
    GET    /api/bus/          → liste tous les bus
    POST   /api/bus/          → créer un bus
    GET    /api/bus/<id>/     → détail d'un bus
    PUT    /api/bus/<id>/     → modifier un bus
    PATCH  /api/bus/<id>/     → modifier partiellement
    DELETE /api/bus/<id>/     → supprimer un bus
    GET    /api/bus/actifs/   → liste des bus actifs seulement
    """
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    # Recherche par immatriculation et filtrage par statut
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['immatriculation']
    ordering_fields = ['immatriculation', 'nombre_places', 'statut']

    def get_permissions(self):
        """
        Lecture accessible à tous, modification réservée aux administrateurs.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='actifs')
    def actifs(self, request):
        """
        Action personnalisée : retourne uniquement les bus actifs.
        GET /api/bus/actifs/
        Utilisée par l'app Trajets pour sélectionner un bus disponible.
        """
        bus_actifs = Bus.objects.filter(statut='ACTIF')
        serializer = self.get_serializer(bus_actifs, many=True)
        return Response({
            'count': bus_actifs.count(),
            'bus_actifs': serializer.data
        })
