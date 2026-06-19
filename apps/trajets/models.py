from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import date
from apps.bus.models import Bus

class Trajet(models.Model):
    ville_depart = models.CharField(max_length=100, verbose_name="Ville de départ")
    ville_arrivee = models.CharField(max_length=100, verbose_name="Ville d'arrivée")
    date_depart = models.DateField(verbose_name="Date de départ")
    heure_depart = models.TimeField(verbose_name="Heure de départ")
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT, related_name='trajets')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        ordering = ['date_depart', 'heure_depart']
        unique_together = [['bus', 'date_depart', 'heure_depart']]

    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee} - {self.date_depart} {self.heure_depart}"

    def clean(self):
        if self.bus_id:
            try:
                bus = Bus.objects.get(pk=self.bus_id)
                if bus.statut != 'ACTIF':
                    raise ValidationError({'bus': f'Le bus {bus.immatriculation} doit être ACTIF'})
            except Bus.DoesNotExist:
                pass
        if self.ville_depart and self.ville_arrivee:
            if self.ville_depart.strip().lower() == self.ville_arrivee.strip().lower():
                raise ValidationError({'ville_arrivee': 'La ville d\'arrivée doit être différente'})

    def get_places_reservees(self):
        from django.db.models import Sum
        total = self.reservations.filter(statut__in=['EN_ATTENTE', 'CONFIRMEE']).aggregate(total=Sum('nombre_places'))['total']
        return total or 0

    def get_places_disponibles(self):
        return self.bus.nombre_places - self.get_places_reservees()

    def est_complet(self):
        return self.get_places_disponibles() <= 0

    def est_passe(self):
        return self.date_depart < date.today()

    def get_taux_remplissage(self):
        if self.bus.nombre_places == 0:
            return 0
        return int((self.get_places_reservees() / self.bus.nombre_places) * 100)
