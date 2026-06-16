"""
Configuration de l'interface d'administration Django pour l'app Bus.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Bus


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    """
    Administration personnalisée du modèle Bus.
    Offre une vue claire de la flotte avec filtres et recherche.
    """

    # Colonnes affichées dans la liste
    list_display = [
        'immatriculation', 'nombre_places', 'badge_statut',
        'get_nombre_trajets', 'date_creation', 'date_modification'
    ]

    # Champs de recherche
    search_fields = ['immatriculation', 'notes']

    # Filtres dans la barre latérale droite
    list_filter = ['statut', 'date_creation']

    # Colonnes triables
    ordering = ['immatriculation']

    # Champs en lecture seule (gérés automatiquement par Django)
    readonly_fields = ['date_creation', 'date_modification']

    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Informations du véhicule', {
            'fields': ('immatriculation', 'nombre_places', 'statut')
        }),
        ('Notes internes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',),
        }),
    )

    # Filtres de date
    date_hierarchy = 'date_creation'

    def badge_statut(self, obj):
        """Affiche le statut sous forme de badge coloré selon l'état."""
        couleurs = {
            'ACTIF': '#28a745',        # Vert
            'INACTIF': '#6c757d',      # Gris
            'MAINTENANCE': '#ffc107',  # Orange/Jaune
        }
        couleur = couleurs.get(obj.statut, '#6c757d')
        return format_html(
            '<span style="background-color:{}; color:{}; padding:3px 10px; '
            'border-radius:12px; font-size:12px; font-weight:bold;">{}</span>',
            couleur,
            'white' if obj.statut != 'MAINTENANCE' else '#333',
            obj.get_statut_display()
        )
    badge_statut.short_description = "Statut"
    badge_statut.allow_tags = True

    def get_nombre_trajets(self, obj):
        """Retourne le nombre de trajets avec un lien vers le filtre."""
        count = obj.get_nombre_trajets()
        return f"{count} trajet(s)"
    get_nombre_trajets.short_description = "Trajets"

    # Actions d'administration personnalisées
    actions = ['marquer_actif', 'marquer_maintenance', 'marquer_inactif']

    def marquer_actif(self, request, queryset):
        """Met les bus sélectionnés en statut ACTIF."""
        modifies = queryset.update(statut='ACTIF')
        self.message_user(request, f"{modifies} bus marqué(s) comme ACTIF.")
    marquer_actif.short_description = "✅ Marquer comme ACTIF"

    def marquer_maintenance(self, request, queryset):
        """Met les bus sélectionnés en statut MAINTENANCE."""
        modifies = queryset.update(statut='MAINTENANCE')
        self.message_user(request, f"{modifies} bus mis en MAINTENANCE.")
    marquer_maintenance.short_description = "🔧 Mettre en MAINTENANCE"

    def marquer_inactif(self, request, queryset):
        """Met les bus sélectionnés en statut INACTIF."""
        modifies = queryset.update(statut='INACTIF')
        self.message_user(request, f"{modifies} bus marqué(s) comme INACTIF.")
    marquer_inactif.short_description = "❌ Marquer comme INACTIF"
