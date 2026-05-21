"""
Configuration de l'interface d'administration Django pour l'app Comptes.
Personnalise l'affichage des utilisateurs dans l'admin.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Administration personnalisée du modèle User.
    Étend UserAdmin pour inclure nos champs supplémentaires.
    """

    # Colonnes affichées dans la liste des utilisateurs
    list_display = [
        'email', 'prenom', 'nom', 'telephone',
        'date_inscription', 'is_active', 'is_staff',
        'badge_reservations'
    ]

    # Champs permettant la recherche rapide
    search_fields = ['email', 'prenom', 'nom', 'username', 'telephone']

    # Filtres dans la barre latérale
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_inscription']

    # Tri par défaut
    ordering = ['-date_inscription']

    # Champs cliquables pour accéder au détail
    list_display_links = ['email', 'prenom']

    # Filtres de date dans la barre latérale
    date_hierarchy = 'date_inscription'

    # Organisation des champs dans le formulaire de modification
    fieldsets = (
        # Section : Identifiants
        ('Identifiants de connexion', {
            'fields': ('username', 'email', 'password')
        }),
        # Section : Informations personnelles
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'telephone')
        }),
        # Section : Permissions et droits
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),  # Section repliable
        }),
        # Section : Dates importantes
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )

    # Champs pour le formulaire d'AJOUT d'un utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'prenom', 'nom', 'telephone',
                'password1', 'password2', 'is_active', 'is_staff'
            ),
        }),
    )

    # Champs en lecture seule
    readonly_fields = ['date_inscription', 'last_login', 'date_joined']

    def badge_reservations(self, obj):
        """Affiche le nombre de réservations sous forme de badge coloré."""
        count = obj.get_nombre_reservations()
        couleur = '#28a745' if count > 0 else '#6c757d'
        return format_html(
            '<span style="background-color:{}; color:white; padding:2px 8px; '
            'border-radius:12px; font-size:12px;">{} réservation(s)</span>',
            couleur, count
        )
    badge_reservations.short_description = "Réservations"
    badge_reservations.allow_tags = True
