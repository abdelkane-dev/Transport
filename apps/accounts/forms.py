"""
Formulaires de l'application Comptes.
Gère l'inscription, la connexion et la modification du profil.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Récupère notre modèle User personnalisé
User = get_user_model()


class InscriptionForm(forms.ModelForm):
    """
    Formulaire d'inscription d'un nouvel utilisateur.
    Inclut la validation du mot de passe et la confirmation.
    """

    # Champ mot de passe avec masquage (PasswordInput)
    mot_de_passe = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Au moins 8 caractères',
            'autocomplete': 'new-password',
        }),
        min_length=8,
        help_text="Minimum 8 caractères, ne peut pas être entièrement numérique."
    )

    # Champ confirmation du mot de passe
    confirmer_mot_de_passe = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Répétez votre mot de passe',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = User
        # Champs à afficher dans le formulaire
        fields = ['prenom', 'nom', 'email', 'telephone', 'username']
        widgets = {
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom de famille',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemple@email.com',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221771234567',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Identifiant unique (ex: jean_dupont)',
            }),
        }
        labels = {
            'prenom': 'Prénom',
            'nom': 'Nom de famille',
            'email': 'Adresse e-mail',
            'telephone': 'Téléphone',
            'username': "Nom d'utilisateur",
        }
        help_texts = {
            'username': "150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement.",
        }

    def clean_email(self):
        """Vérifie que l'email n'est pas déjà utilisé."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Cette adresse e-mail est déjà associée à un compte. "
                "Veuillez vous connecter ou utiliser une autre adresse."
            )
        return email

    def clean(self):
        """Validation globale : vérifier que les deux mots de passe correspondent."""
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get('mot_de_passe')
        confirmer = cleaned_data.get('confirmer_mot_de_passe')

        if mot_de_passe and confirmer and mot_de_passe != confirmer:
            raise ValidationError({
                'confirmer_mot_de_passe': "Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau."
            })
        return cleaned_data

    def save(self, commit=True):
        """Sauvegarde l'utilisateur avec le mot de passe hashé correctement."""
        user = super().save(commit=False)
        # Utilise set_password() pour hasher le mot de passe (jamais en clair)
        user.set_password(self.cleaned_data['mot_de_passe'])
        if commit:
            user.save()
        return user


class ConnexionForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé.
    Utilise AuthenticationForm de Django avec nos classes CSS.
    """

    # Remplacer le champ username par email
    username = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe',
        })
    )

    error_messages = {
        'invalid_login': (
            "Adresse e-mail ou mot de passe incorrect. "
            "Veuillez réessayer."
        ),
        'inactive': "Ce compte est désactivé. Contactez l'administrateur.",
    }


class ProfilForm(forms.ModelForm):
    """
    Formulaire de modification du profil utilisateur.
    Ne permet pas de modifier l'email (identifiant de connexion).
    """

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'telephone']
        widgets = {
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221771234567',
            }),
        }
