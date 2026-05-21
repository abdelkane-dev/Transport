"""
Serializers DRF pour l'application Trajets.
"""

from rest_framework import serializers
from .models import Trajet
from apps.bus.serializers import BusSerializer
from apps.bus.models import Bus


class TrajetSerializer(serializers.ModelSerializer):
    """
    Serializer complet pour le modèle Trajet.
    """
    # Informations du bus (en lecture seule pour l'affichage)
    bus_detail = BusSerializer(source='bus', read_only=True)
    # Champs calculés
    places_disponibles = serializers.SerializerMethodField()
    places_reservees = serializers.SerializerMethodField()
    est_complet = serializers.BooleanField(read_only=True)
    est_passe = serializers.BooleanField(read_only=True)
    taux_remplissage = serializers.SerializerMethodField()
    prix_formate = serializers.SerializerMethodField()

    class Meta:
        model = Trajet
        fields = [
            'id', 'ville_depart', 'ville_arrivee', 'date_depart', 'heure_depart',
            'prix', 'prix_formate', 'bus', 'bus_detail',
            'places_disponibles', 'places_reservees', 'est_complet', 'est_passe',
            'taux_remplissage', 'date_creation', 'date_modification'
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']

    def get_places_disponibles(self, obj):
        return obj.get_places_disponibles()

    def get_places_reservees(self, obj):
        return obj.get_places_reservees()

    def get_taux_remplissage(self, obj):
        return obj.get_taux_remplissage()

    def get_prix_formate(self, obj):
        """Formate le prix avec séparateur de milliers."""
        return f"{obj.prix:,.0f} FCFA"

    def validate_bus(self, value):
        """Vérifie que le bus assigné est bien ACTIF."""
        if not value.est_actif():
            raise serializers.ValidationError(
                f"Le bus '{value.immatriculation}' n'est pas ACTIF "
                f"(statut actuel : {value.get_statut_display()}). "
                "Veuillez sélectionner un bus actif."
            )
        return value

    def validate(self, data):
        """Vérifie que les villes de départ et d'arrivée sont différentes."""
        if 'ville_depart' in data and 'ville_arrivee' in data:
            if data['ville_depart'].strip().lower() == data['ville_arrivee'].strip().lower():
                raise serializers.ValidationError({
                    'ville_arrivee': "La ville d'arrivée doit être différente de la ville de départ."
                })
        return data
