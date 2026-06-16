"""
Modèles de l'application Réservations.
Définit le modèle Reservation liant un client à un trajet.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.conf import settings
from apps.trajets.models import Trajet


class Reservation(models.Model):
    """
    Modèle représentant une réservation de places sur un trajet.

    Règles métier :
    1. Il doit rester suffisamment de places avant de réserver
    2. Le statut initial est EN_ATTENTE (en attente de confirmation)
    3. Un client ne peut annuler que si le trajet n'est pas encore passé
    4. Chaque client ne voit que ses propres réservations

    Relations :
    - client  : ForeignKey vers User (le client qui réserve)
    - trajet  : ForeignKey vers Trajet (le trajet réservé)
    """

    # -------------------------------------------------------
    # CHOIX DU STATUT
    # -------------------------------------------------------
    class StatutReservation(models.TextChoices):
        EN_ATTENTE = 'EN_ATTENTE', 'En attente'
        CONFIRMEE = 'CONFIRMEE', 'Confirmée'
        ANNULEE = 'ANNULEE', 'Annulée'

    # -------------------------------------------------------
    # CHAMPS DU MODÈLE
    # -------------------------------------------------------

    # Client qui fait la réservation (lié à notre User personnalisé)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Client",
        help_text="Utilisateur qui effectue la réservation."
    )

    # Trajet réservé
    trajet = models.ForeignKey(
        Trajet,
        on_delete=models.PROTECT,  # Protège contre la suppression du trajet si réservé
        related_name='reservations',
        verbose_name="Trajet",
        help_text="Le trajet pour lequel la réservation est faite."
    )

    # Nombre de places réservées (au moins 1)
    nombre_places = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Nombre de places",
        help_text="Nombre de places à réserver (minimum 1)."
    )

    # Date/heure de la réservation (automatique à la création)
    date_reservation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de réservation"
    )

    # Statut de la réservation
    statut = models.CharField(
        max_length=15,
        choices=StatutReservation.choices,
        default=StatutReservation.EN_ATTENTE,
        verbose_name="Statut",
        help_text="État actuel de la réservation."
    )

    # Notes libres (raison d'annulation, demandes spéciales, etc.)
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name="Notes",
        help_text="Commentaires ou raison d'annulation (optionnel)."
    )

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date_reservation']

    def __str__(self):
        """Représentation : 'Alice Dupont – Dakar→Thiès (15/06/2024) – 2 place(s)'"""
        return (
            f"{self.client.get_full_name()} – "
            f"{self.trajet.ville_depart}→{self.trajet.ville_arrivee} "
            f"({self.trajet.date_depart}) – "
            f"{self.nombre_places} place(s) [{self.get_statut_display()}]"
        )

    def clean(self):
        """
        Validation métier lors de la création/modification d'une réservation.

        Règles vérifiées :
        1. Il doit rester assez de places sur le trajet
        2. Le trajet ne doit pas être passé (on ne réserve pas dans le passé)
        3. Le nombre de places demandé doit être >= 1
        """
        # Vérification uniquement si le trajet et le nombre de places sont définis
        if not self.trajet_id or not self.nombre_places:
            return

        # Règle 1 : Vérifier que le trajet n'est pas passé
        if self.trajet.est_passe():
            raise ValidationError(
                "Impossible de réserver un trajet dont la date est déjà passée."
            )

        # Règle 2 : Vérifier les places disponibles
        # Pour la modification, exclure les places déjà réservées par CETTE réservation
        places_reservees = self.trajet.reservations.filter(
            statut__in=['EN_ATTENTE', 'CONFIRMEE']
        )
        if self.pk:
            # On modifie une réservation existante → exclure soi-même du calcul
            places_reservees = places_reservees.exclude(pk=self.pk)

        from django.db.models import Sum
        total_reservees = places_reservees.aggregate(
            total=Sum('nombre_places')
        )['total'] or 0

        places_disponibles = self.trajet.bus.nombre_places - total_reservees

        if self.nombre_places > places_disponibles:
            raise ValidationError(
                f"Pas assez de places disponibles. "
                f"Vous demandez {self.nombre_places} place(s) mais seulement "
                f"{places_disponibles} place(s) sont disponibles sur ce trajet."
            )

    def peut_etre_annulee(self):
        """
        Vérifie si la réservation peut encore être annulée.
        Conditions : statut pas déjà ANNULEE et trajet pas encore passé.
        """
        if self.statut == self.StatutReservation.ANNULEE:
            return False
        return not self.trajet.est_passe()

    def get_prix_total(self):
        """Calcule le prix total de la réservation."""
        return self.nombre_places * self.trajet.prix

    def annuler(self, raison=''):
        """
        Annule la réservation si les conditions sont remplies.
        Retourne (True, message) en cas de succès, (False, message) en cas d'échec.
        """
        if not self.peut_etre_annulee():
            if self.statut == self.StatutReservation.ANNULEE:
                return False, "Cette réservation est déjà annulée."
            return False, "Impossible d'annuler : le trajet est déjà passé."

        self.statut = self.StatutReservation.ANNULEE
        if raison:
            self.notes = raison
        self.save()
        return True, "Réservation annulée avec succès."

    def confirmer(self):
        """Confirme une réservation EN_ATTENTE. Réservé aux administrateurs."""
        if self.statut != self.StatutReservation.EN_ATTENTE:
            return False, f"La réservation est déjà '{self.get_statut_display()}'."
        self.statut = self.StatutReservation.CONFIRMEE
        self.save()
        return True, "Réservation confirmée avec succès."
