"""
Formulaires de l'application Trajets.
Gère la création et modification des trajets avec validation métier.
"""

from django import forms
from django.utils import timezone
from datetime import date
from .models import Trajet
from apps.bus.models import Bus


class TrajetForm(forms.ModelForm):
    """
    Formulaire de création et modification d'un trajet.
    - Filtre les bus pour n'afficher que les bus ACTIFS
    - Valide que la date de départ est dans le futur (pour les nouveaux trajets)
    """

    class Meta:
        model = Trajet
        fields = ['ville_depart', 'ville_arrivee', 'date_depart', 'heure_depart', 'prix', 'bus']
        widgets = {
            'ville_depart': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Dakar',
            }),
            'ville_arrivee': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Thiès',
            }),
            'date_depart': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',  # Sélecteur de date natif HTML5
                },
                format='%Y-%m-%d'
            ),
            'heure_depart': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time',  # Sélecteur d'heure natif HTML5
                },
                format='%H:%M'
            ),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01',
                'placeholder': 'Ex: 5000',
            }),
            'bus': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'ville_depart': 'Ville de départ',
            'ville_arrivee': 'Ville d\'arrivée',
            'date_depart': 'Date de départ',
            'heure_depart': 'Heure de départ',
            'prix': 'Prix par place (FCFA)',
            'bus': 'Bus assigné',
        }

    def __init__(self, *args, **kwargs):
        """
        Override __init__ pour filtrer le queryset des bus :
        on n'affiche que les bus avec statut ACTIF.
        """
        super().__init__(*args, **kwargs)
        # Filtrer pour n'afficher que les bus actifs dans la liste déroulante
        self.fields['bus'].queryset = Bus.objects.filter(statut='ACTIF')
        self.fields['bus'].empty_label = "--- Sélectionnez un bus actif ---"

    def clean_date_depart(self):
        """
        Valide que la date de départ est dans le futur.
        (Uniquement pour la création, pas la modification)
        """
        date_depart = self.cleaned_data.get('date_depart')
        if date_depart:
            # Pour une création (pas d'instance existante), vérifier le futur
            if not self.instance.pk and date_depart < date.today():
                raise forms.ValidationError(
                    "La date de départ doit être aujourd'hui ou dans le futur."
                )
        return date_depart

    def clean(self):
        """Validation globale : déléguer au modèle (appel clean())."""
        cleaned_data = super().clean()
        ville_depart = cleaned_data.get('ville_depart', '').strip().lower()
        ville_arrivee = cleaned_data.get('ville_arrivee', '').strip().lower()

        if ville_depart and ville_arrivee and ville_depart == ville_arrivee:
            raise forms.ValidationError({
                'ville_arrivee': "La ville d'arrivée doit être différente de la ville de départ."
            })
        return cleaned_data


class RechercheTrajetForm(forms.Form):
    """
    Formulaire de recherche de trajets sur la page d'accueil.
    Permet aux clients de trouver un trajet selon leurs critères.
    """
    ville_depart = forms.CharField(
        required=False,
        label="Ville de départ",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Dakar',
        })
    )
    ville_arrivee = forms.CharField(
        required=False,
        label="Ville d'arrivée",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Thiès',
        })
    )
    date_depart = forms.DateField(
        required=False,
        label="Date de départ",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }, format='%Y-%m-%d')
    )
