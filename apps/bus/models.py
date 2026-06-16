"""
Modèles de l'application Bus.
Définit le modèle Bus représentant les véhicules de la compagnie.
"""

from django.db import models
from django.core.validators import MinValueValidator


class Bus(models.Model):
    """
    Modèle représentant un bus de la flotte.

    Champs :
    - immatriculation : identifiant unique du véhicule (ex: DK-1234-AB)
    - nombre_places   : capacité totale du bus (minimum 1)
    - statut          : état actuel du bus (ACTIF, INACTIF, MAINTENANCE)
    - date_creation   : date d'ajout du bus dans le système
    - notes           : remarques libres sur le bus
    """

    # -------------------------------------------------------
    # CHOIX DU STATUT
    # -------------------------------------------------------
    class StatutBus(models.TextChoices):
        ACTIF = 'ACTIF', 'Actif'
        INACTIF = 'INACTIF', 'Inactif'
        MAINTENANCE = 'MAINTENANCE', 'En maintenance'

    # -------------------------------------------------------
    # CHAMPS DU MODÈLE
    # -------------------------------------------------------

    # Numéro d'immatriculation – doit être unique dans la flotte
    immatriculation = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Immatriculation",
        help_text="Numéro d'immatriculation unique du bus (ex: DK-1234-AB)."
    )

    # Nombre de places assises disponibles
    nombre_places = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Nombre de places",
        help_text="Capacité totale du bus (minimum 1 place)."
    )

    # Statut du bus (ACTIF par défaut pour les nouveaux bus)
    statut = models.CharField(
        max_length=15,
        choices=StatutBus.choices,
        default=StatutBus.ACTIF,
        verbose_name="Statut",
        help_text="État actuel du bus. Seuls les bus ACTIFS peuvent être assignés à des trajets."
    )

    # Date d'ajout automatique dans le système
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'ajout"
    )

    # Date de dernière modification
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    # Notes libres sur le bus (entretien, remarques, etc.)
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name="Notes",
        help_text="Remarques internes sur ce bus (optionnel)."
    )

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Bus"
        ordering = ['immatriculation']  # Tri alphabétique par immatriculation

    def __str__(self):
        """Représentation lisible : 'DK-1234-AB (ACTIF – 50 places)'"""
        return f"{self.immatriculation} ({self.get_statut_display()} – {self.nombre_places} places)"

    def est_actif(self):
        """Retourne True si le bus est en état ACTIF."""
        return self.statut == self.StatutBus.ACTIF

    def get_places_reservees(self, trajet=None):
        """
        Calcule le nombre de places réservées pour un trajet donné.
        Si aucun trajet, retourne 0.
        """
        if trajet is None:
            return 0
        return trajet.reservations.filter(
            statut__in=['EN_ATTENTE', 'CONFIRMEE']
        ).aggregate(
            total=models.Sum('nombre_places')
        )['total'] or 0

    def get_nombre_trajets(self):
        """Retourne le nombre de trajets liés à ce bus."""
        return self.trajets.count()
