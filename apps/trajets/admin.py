"""
Configuration de l'interface d'administration pour l'app Trajets.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import date
from .models import Trajet


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    """
    Administration personnalisée du modèle Trajet.
    Inclut filtres par date, recherche par ville, affichage des disponibilités.
    """

    # Colonnes affichées dans la liste
    list_display = [
        'ville_depart', 'ville_arrivee', 'date_depart', 'heure_depart',
        'bus', 'prix_formate', 'badge_disponibilite', 'badge_statut_trajet'
    ]

    # Champs de recherche
    search_fields = ['ville_depart', 'ville_arrivee', 'bus__immatriculation']

    # Filtres dans la barre latérale
    list_filter = ['date_depart', 'ville_depart', 'ville_arrivee', 'bus__statut']

    # Tri par défaut
    ordering = ['-date_depart', 'heure_depart']

    # Filtre de date hiérarchique (navigation par année/mois/jour)
    date_hierarchy = 'date_depart'

    # Champs en lecture seule
    readonly_fields = ['date_creation', 'date_modification', 'places_disponibles_affichage']

    # Organisation du formulaire
    fieldsets = (
        ('Informations du trajet', {
            'fields': ('ville_depart', 'ville_arrivee', 'date_depart', 'heure_depart')
        }),
        ('Tarification et véhicule', {
            'fields': ('prix', 'bus')
        }),
        ('Disponibilité (lecture seule)', {
            'fields': ('places_disponibles_affichage',),
            'classes': ('collapse',),
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',),
        }),
    )

    def prix_formate(self, obj):
        """Affiche le prix formaté avec le symbole FCFA."""
        return f"{obj.prix:,.0f} FCFA"
    prix_formate.short_description = "Prix"

    def badge_disponibilite(self, obj):
        """Badge coloré montrant les places disponibles."""
        dispo = obj.get_places_disponibles()
        total = obj.bus.nombre_places
        reservees = obj.get_places_reservees()

        if dispo <= 0:
            couleur = '#dc3545'
            texte = "Complet"
        elif dispo <= total * 0.2:
            couleur = '#ffc107'
            texte = f"{dispo} place(s)"
        else:
            couleur = '#28a745'
            texte = f"{dispo}/{total} places"

        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:10px;font-size:11px;">{}</span>',
            couleur, texte
        )
    badge_disponibilite.short_description = "Disponibilité"

    def badge_statut_trajet(self, obj):
        """Indique si le trajet est passé ou à venir."""
        if obj.est_passe():
            return format_html(
                '<span style="color:#6c757d;font-size:11px;">✓ Passé</span>'
            )
        return format_html(
            '<span style="color:#28a745;font-size:11px;">→ À venir</span>'
        )
    badge_statut_trajet.short_description = "État"

    def places_disponibles_affichage(self, obj):
        """Affichage des places dans le formulaire de détail."""
        if obj.pk:
            return (
                f"{obj.get_places_disponibles()} places disponibles sur "
                f"{obj.bus.nombre_places} (réservées : {obj.get_places_reservees()})"
            )
        return "Disponible après sauvegarde"
    places_disponibles_affichage.short_description = "Places disponibles"
