"""
Serializers DRF pour l'application Comptes.
Convertit les instances User en JSON et vice-versa.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer de base pour afficher les informations d'un utilisateur.
    Ne contient pas le mot de passe (sécurité).
    """
    # Champ calculé : nom complet
    nom_complet = serializers.SerializerMethodField()
    # Nombre de réservations (champ en lecture seule)
    nombre_reservations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'prenom', 'nom', 'nom_complet',
            'telephone', 'date_inscription', 'nombre_reservations', 'is_active'
        ]
        # Ces champs ne peuvent pas être modifiés via l'API
        read_only_fields = ['id', 'email', 'date_inscription', 'nombre_reservations']

    def get_nom_complet(self, obj):
        """Retourne le nom complet 'Prénom Nom'."""
        return obj.get_full_name()

    def get_nombre_reservations(self, obj):
        """Retourne le nombre total de réservations."""
        return obj.get_nombre_reservations()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouvel utilisateur.
    Gère la validation du mot de passe et sa confirmation.
    """
    mot_de_passe = serializers.CharField(
        write_only=True,       # Ne jamais renvoyer le mot de passe dans la réponse
        min_length=8,
        style={'input_type': 'password'},
        label="Mot de passe"
    )
    confirmer_mot_de_passe = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        label="Confirmer le mot de passe"
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'prenom', 'nom', 'telephone',
            'mot_de_passe', 'confirmer_mot_de_passe'
        ]

    def validate_email(self, value):
        """Vérifie que l'email est unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Cette adresse e-mail est déjà utilisée."
            )
        return value

    def validate(self, data):
        """Vérifie que les deux mots de passe correspondent."""
        if data['mot_de_passe'] != data['confirmer_mot_de_passe']:
            raise serializers.ValidationError({
                'confirmer_mot_de_passe': "Les mots de passe ne correspondent pas."
            })
        return data

    def create(self, validated_data):
        """Crée l'utilisateur avec le mot de passe correctement hashé."""
        # Retirer les champs non-model avant la création
        validated_data.pop('confirmer_mot_de_passe')
        mot_de_passe = validated_data.pop('mot_de_passe')

        user = User(**validated_data)
        user.set_password(mot_de_passe)  # Hashing sécurisé
        user.save()
        return user
