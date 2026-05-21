"""
Configuration de l'interface d'administration pour l'app Réservations.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Administration personnalisée du modèle Reservation.
    """

    # Colonnes de la liste
    list_display = [
        'id', 'client_nom', 'trajet_info', 'nombre_places',
        'prix_total_affichage', 'badge_statut', 'date_reservation'
    ]

    # Champs de recherche
    search_fields = [
        'client__nom', 'client__prenom', 'client__email',
        'trajet__ville_depart', 'trajet__ville_arrivee'
    ]

    # Filtres dans la barre latérale
    list_filter = ['statut', 'date_reservation', 'trajet__ville_depart']

    # Tri par défaut
    ordering = ['-date_reservation']

    # Hiérarchie par date
    date_hierarchy = 'date_reservation'

    # Champs en lecture seule
    readonly_fields = ['date_reservation', 'prix_total_affichage']

    # Organisation du formulaire
    fieldsets = (
        ('Informations de réservation', {
            'fields': ('client', 'trajet', 'nombre_places')
        }),
        ('Statut', {
            'fields': ('statut', 'notes')
        }),
        ('Informations calculées', {
            'fields': ('prix_total_affichage', 'date_reservation'),
            'classes': ('collapse',),
        }),
    )

    def client_nom(self, obj):
        """Affiche le nom complet du client."""
        return obj.client.get_full_name()
    client_nom.short_description = "Client"

    def trajet_info(self, obj):
        """Affiche un résumé du trajet."""
        return f"{obj.trajet.ville_depart} → {obj.trajet.ville_arrivee} ({obj.trajet.date_depart})"
    trajet_info.short_description = "Trajet"

    def badge_statut(self, obj):
        """Badge coloré selon le statut."""
        couleurs = {
            'EN_ATTENTE': '#ffc107',
            'CONFIRMEE': '#28a745',
            'ANNULEE': '#dc3545',
        }
        couleur = couleurs.get(obj.statut, '#6c757d')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:10px;font-size:11px;">{}</span>',
            couleur, obj.get_statut_display()
        )
    badge_statut.short_description = "Statut"

    def prix_total_affichage(self, obj):
        """Affiche le prix total calculé."""
        if obj.pk:
            return f"{obj.get_prix_total():,.0f} FCFA"
        return "N/A"
    prix_total_affichage.short_description = "Prix total"

    # Actions d'administration
    actions = ['confirmer_reservations', 'annuler_reservations']

    def confirmer_reservations(self, request, queryset):
        """Confirme toutes les réservations EN_ATTENTE sélectionnées."""
        confirmees = 0
        for reservation in queryset.filter(statut='EN_ATTENTE'):
            succes, _ = reservation.confirmer()
            if succes:
                confirmees += 1
        self.message_user(request, f"{confirmees} réservation(s) confirmée(s).")
    confirmer_reservations.short_description = "✅ Confirmer les réservations sélectionnées"

    def annuler_reservations(self, request, queryset):
        """Annule les réservations sélectionnées (si possible)."""
        annulees = 0
        for reservation in queryset:
            succes, _ = reservation.annuler()
            if succes:
                annulees += 1
        self.message_user(request, f"{annulees} réservation(s) annulée(s).")
    annuler_reservations.short_description = "❌ Annuler les réservations sélectionnées"
