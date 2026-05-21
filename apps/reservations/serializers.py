"""
Serializers DRF pour l'application Réservations.
"""

from rest_framework import serializers
from .models import Reservation
from apps.trajets.serializers import TrajetSerializer
from apps.accounts.serializers import UserSerializer


class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer complet pour le modèle Reservation.
    """
    # Détails du trajet et du client (lecture seule)
    trajet_detail = TrajetSerializer(source='trajet', read_only=True)
    client_detail = UserSerializer(source='client', read_only=True)
    # Champs calculés
    prix_total = serializers.SerializerMethodField()
    peut_etre_annulee = serializers.BooleanField(read_only=True)
    statut_libelle = serializers.CharField(source='get_statut_display', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'client', 'client_detail', 'trajet', 'trajet_detail',
            'nombre_places', 'date_reservation', 'statut', 'statut_libelle',
            'prix_total', 'peut_etre_annulee', 'notes'
        ]
        read_only_fields = ['id', 'date_reservation', 'client']

    def get_prix_total(self, obj):
        """Calcule et formate le prix total."""
        total = obj.get_prix_total()
        return f"{total:,.0f} FCFA"

    def validate(self, data):
        """Valide les règles métier via le modèle."""
        # Récupérer l'instance temporaire pour appeler clean()
        instance = Reservation(**data)
        if self.instance:
            # Modification : copier les valeurs existantes
            for field in ['client', 'trajet']:
                if field not in data:
                    setattr(instance, field, getattr(self.instance, field))
            instance.pk = self.instance.pk

        try:
            instance.clean()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return data

    def create(self, validated_data):
        """Crée une réservation en assignant automatiquement le client connecté."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['client'] = request.user
        return super().create(validated_data)
