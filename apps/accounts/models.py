"""
Modèles de l'application Comptes (Accounts).
Définit le modèle User personnalisé qui étend AbstractUser de Django.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


# Validateur pour les numéros de téléphone (format africain typique)
telephone_validator = RegexValidator(
    regex=r'^\+?[0-9]{8,15}$',
    message="Le numéro de téléphone doit contenir entre 8 et 15 chiffres, avec ou sans le préfixe +."
)


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    Étend AbstractUser pour ajouter des champs supplémentaires :
    nom, prenom, email (obligatoire et unique), telephone.

    Note : on garde 'first_name' et 'last_name' de AbstractUser,
    mais on ajoute 'nom' et 'prenom' en français pour clarté.
    En pratique, on utilise nos champs et on masque les champs Django.
    """

    # Champ email rendu obligatoire et unique (AbstractUser le rend optionnel par défaut)
    email = models.EmailField(
        unique=True,
        verbose_name="Adresse e-mail",
        help_text="Adresse e-mail valide, utilisée pour la connexion."
    )

    # Prénom du client
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
        help_text="Prénom du client."
    )

    # Nom de famille du client
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom de famille",
        help_text="Nom de famille du client."
    )

    # Numéro de téléphone (optionnel mais recommandé)
    telephone = models.CharField(
        max_length=20,
        validators=[telephone_validator],
        blank=True,
        null=True,
        verbose_name="Numéro de téléphone",
        help_text="Numéro de téléphone au format international (ex: +221771234567)."
    )

    # Date d'inscription automatique
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )

    # Utiliser l'email comme identifiant de connexion au lieu du username
    USERNAME_FIELD = 'email'
    # Champs requis lors de la création via createsuperuser
    REQUIRED_FIELDS = ['username', 'nom', 'prenom']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_inscription']

    def __str__(self):
        """Représentation lisible de l'utilisateur."""
        return f"{self.prenom} {self.nom} ({self.email})"

    def get_full_name(self):
        """Retourne le nom complet formaté."""
        return f"{self.prenom} {self.nom}".strip()

    def get_nombre_reservations(self):
        """Retourne le nombre total de réservations du client."""
        return self.reservations.count()

    def get_reservations_actives(self):
        """Retourne les réservations non annulées du client."""
        return self.reservations.exclude(statut='ANNULEE')
