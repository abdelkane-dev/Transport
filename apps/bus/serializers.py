"""
Serializers DRF pour l'application Bus.
"""

from rest_framework import serializers
from .models import Bus


class BusSerializer(serializers.ModelSerializer):
    """
    Serializer complet pour le modèle Bus.
    Utilisé pour les opérations CRUD via l'API.
    """
    # Champ calculé : libellé du statut (ex: 'En maintenance' au lieu de 'MAINTENANCE')
    statut_libelle = serializers.CharField(source='get_statut_display', read_only=True)
    # Nombre de trajets liés
    nombre_trajets = serializers.SerializerMethodField()
    # Indique si le bus est actif
    est_actif = serializers.BooleanField(read_only=True)

    class Meta:
        model = Bus
        fields = [
            'id', 'immatriculation', 'nombre_places', 'statut', 'statut_libelle',
            'est_actif', 'nombre_trajets', 'notes', 'date_creation', 'date_modification'
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']

    def get_nombre_trajets(self, obj):
        """Retourne le nombre de trajets pour ce bus."""
        return obj.get_nombre_trajets()

    def validate_immatriculation(self, value):
        """Mettre en majuscule et vérifier l'unicité."""
        value = value.upper().strip()
        qs = Bus.objects.filter(immatriculation=value)
        # Exclure le bus en cours de modification
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f"Un bus avec l'immatriculation '{value}' existe déjà."
            )
        return value
