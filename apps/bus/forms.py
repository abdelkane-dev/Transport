"""
Formulaires de l'application Bus.
Gère la création et modification des bus.
"""

from django import forms
from .models import Bus


class BusForm(forms.ModelForm):
    """
    Formulaire de création et modification d'un bus.
    Tous les champs sont rendus accessibles avec les classes Bootstrap.
    """

    class Meta:
        model = Bus
        fields = ['immatriculation', 'nombre_places', 'statut', 'notes']
        widgets = {
            'immatriculation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: DK-1234-AB',
                'style': 'text-transform:uppercase',
            }),
            'nombre_places': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '200',
                'placeholder': 'Ex: 50',
            }),
            'statut': forms.Select(attrs={
                'class': 'form-select',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Remarques internes sur ce bus (optionnel)...',
            }),
        }
        labels = {
            'immatriculation': 'Numéro d\'immatriculation',
            'nombre_places': 'Nombre de places',
            'statut': 'Statut du bus',
            'notes': 'Notes / Remarques',
        }

    def clean_immatriculation(self):
        """Mettre l'immatriculation en majuscules et vérifier l'unicité."""
        immatriculation = self.cleaned_data.get('immatriculation', '').upper().strip()
        # Vérifier l'unicité (sauf si on modifie le même bus)
        qs = Bus.objects.filter(immatriculation=immatriculation)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                f"Un bus avec l'immatriculation '{immatriculation}' existe déjà."
            )
        return immatriculation

    def clean_nombre_places(self):
        """Vérifie que le nombre de places est dans une plage raisonnable."""
        nb = self.cleaned_data.get('nombre_places')
        if nb is not None:
            if nb < 1:
                raise forms.ValidationError("Le bus doit avoir au moins 1 place.")
            if nb > 200:
                raise forms.ValidationError(
                    "Un bus ne peut pas avoir plus de 200 places."
                )
        return nb
