"""
Formulaires de l'application Réservations.
"""

from django import forms
from .models import Reservation
from apps.trajets.models import Trajet


class ReservationForm(forms.ModelForm):
    """
    Formulaire de création d'une réservation.
    - Le client et le trajet sont préremplis (pas visibles par l'utilisateur)
    - Seul le nombre de places est saisi
    """

    class Meta:
        model = Reservation
        fields = ['nombre_places', 'notes']
        widgets = {
            'nombre_places': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'value': '1',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Demandes spéciales ou commentaires (optionnel)...',
            }),
        }
        labels = {
            'nombre_places': 'Nombre de places',
            'notes': 'Commentaires',
        }

    def __init__(self, *args, trajet=None, **kwargs):
        """
        Accepte le trajet en paramètre pour valider le nombre de places.
        Le trajet est stocké dans le formulaire pour les validations.
        """
        super().__init__(*args, **kwargs)
        self.trajet = trajet
        if trajet:
            places_dispo = trajet.get_places_disponibles()
            # Limiter le max de places à ce qui est disponible
            self.fields['nombre_places'].widget.attrs['max'] = str(min(places_dispo, 10))
            self.fields['nombre_places'].help_text = (
                f"Places disponibles sur ce trajet : {places_dispo}"
            )

    def clean_nombre_places(self):
        """Vérifie que le nombre de places demandé est valide."""
        nb = self.cleaned_data.get('nombre_places')
        if nb is None or nb < 1:
            raise forms.ValidationError("Vous devez réserver au moins 1 place.")

        if self.trajet:
            places_dispo = self.trajet.get_places_disponibles()
            if nb > places_dispo:
                raise forms.ValidationError(
                    f"Seulement {places_dispo} place(s) disponibles sur ce trajet. "
                    f"Vous avez demandé {nb} place(s)."
                )
        return nb


class AnnulationForm(forms.Form):
    """
    Formulaire simple de confirmation d'annulation.
    Permet d'ajouter une raison d'annulation.
    """
    raison = forms.CharField(
        required=False,
        label="Raison de l'annulation",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Expliquez pourquoi vous annulez (optionnel)...',
        }),
        max_length=500
    )


class AdminReservationForm(forms.ModelForm):
    """
    Formulaire de réservation pour les administrateurs.
    Permet de définir tous les champs, y compris le client et le statut.
    """

    class Meta:
        model = Reservation
        fields = ['client', 'trajet', 'nombre_places', 'statut', 'notes']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'trajet': forms.Select(attrs={'class': 'form-select'}),
            'nombre_places': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
