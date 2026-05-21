"""
Modèles de l'application Trajets.
Définit le modèle Trajet représentant un voyage planifié d'une ville à une autre.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.bus.models import Bus


class Trajet(models.Model):
    """
    Modèle représentant un trajet planifié.

    Un trajet est une liaison entre deux villes à une date et heure données,
    effectuée par un bus spécifique. Le prix est fixé par trajet.

    Relations :
    - bus : ForeignKey vers Bus (un bus peut avoir plusieurs trajets)
    - reservations : relation inverse (accès via trajet.reservations.all())
    """

    # -------------------------------------------------------
    # CHAMPS DU MODÈLE
    # -------------------------------------------------------

    # Ville de départ
    ville_depart = models.CharField(
        max_length=100,
        verbose_name="Ville de départ",
        help_text="Nom de la ville ou localité de départ."
    )

    # Ville d'arrivée
    ville_arrivee = models.CharField(
        max_length=100,
        verbose_name="Ville d'arrivée",
        help_text="Nom de la ville ou localité d'arrivée."
    )

    # Date du trajet (sans heure)
    date_depart = models.DateField(
        verbose_name="Date de départ",
        help_text="Date prévue du départ (format: JJ/MM/AAAA)."
    )

    # Heure du départ (sans date)
    heure_depart = models.TimeField(
        verbose_name="Heure de départ",
        help_text="Heure prévue du départ (format: HH:MM)."
    )

    # Prix du billet par place (en FCFA ou autre devise)
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Prix (par place)",
        help_text="Prix d'une place en FCFA. Minimum 0,01."
    )

    # Bus assigné à ce trajet (ForeignKey avec protection)
    bus = models.ForeignKey(
        Bus,
        on_delete=models.PROTECT,  # Empêche la suppression du bus si trajet lié
        related_name='trajets',
        verbose_name="Bus assigné",
        help_text="Sélectionnez un bus ACTIF pour ce trajet."
    )

    # Date/heure de création de l'enregistrement
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    # Date/heure de dernière modification
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    class Meta:
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        # Tri : trajets à venir en premier, puis par heure
        ordering = ['-date_depart', 'heure_depart']
        # Contrainte : pas deux fois le même bus au même moment
        unique_together = [['bus', 'date_depart', 'heure_depart']]

    def __str__(self):
        """Représentation : 'Dakar → Thiès | 15/06/2024 à 08h00'"""
        return (
            f"{self.ville_depart} → {self.ville_arrivee} | "
            f"{self.date_depart.strftime('%d/%m/%Y')} à "
            f"{self.heure_depart.strftime('%Hh%M')}"
        )

    def clean(self):
        """
        Validation métier :
        1. Le bus assigné doit être en statut ACTIF
        2. La ville de départ et d'arrivée doivent être différentes
        """
        # Vérification 1 : le bus doit être ACTIF
        if self.bus_id:
            try:
                bus = Bus.objects.get(pk=self.bus_id)
                if not bus.est_actif():
                    raise ValidationError({
                        'bus': (
                            f"Le bus '{bus.immatriculation}' est actuellement '{bus.get_statut_display()}'. "
                            "Seuls les bus ACTIFS peuvent être assignés à un trajet."
                        )
                    })
            except Bus.DoesNotExist:
                pass

        # Vérification 2 : les villes doivent être différentes
        if self.ville_depart and self.ville_arrivee:
            if self.ville_depart.strip().lower() == self.ville_arrivee.strip().lower():
                raise ValidationError({
                    'ville_arrivee': "La ville d'arrivée doit être différente de la ville de départ."
                })

    def get_places_reservees(self):
        """
        Calcule le nombre de places actuellement réservées (EN_ATTENTE + CONFIRMEE).
        Ne compte pas les réservations annulées.
        """
        from django.db.models import Sum
        total = self.reservations.filter(
            statut__in=['EN_ATTENTE', 'CONFIRMEE']
        ).aggregate(total=Sum('nombre_places'))['total']
        return total or 0

    def get_places_disponibles(self):
        """Calcule les places encore disponibles sur ce trajet."""
        return self.bus.nombre_places - self.get_places_reservees()

    def est_complet(self):
        """Retourne True si toutes les places sont réservées."""
        return self.get_places_disponibles() <= 0

    def est_passe(self):
        """Retourne True si la date du trajet est déjà passée."""
        from django.utils import timezone
        from datetime import datetime, date
        return self.date_depart < date.today()

    def get_taux_remplissage(self):
        """Calcule le taux de remplissage en pourcentage."""
        if self.bus.nombre_places == 0:
            return 0
        return int((self.get_places_reservees() / self.bus.nombre_places) * 100)
