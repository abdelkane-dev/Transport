"""
Tests de l'application Comptes.
Couvre : inscription, connexion, déconnexion, profil.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class InscriptionTestCase(TestCase):
    """Tests du processus d'inscription."""

    def setUp(self):
        """Initialisation avant chaque test."""
        self.client = Client()
        self.url_inscription = reverse('accounts:inscription')

    def test_affichage_formulaire_inscription(self):
        """Vérifie que la page d'inscription s'affiche correctement."""
        response = self.client.get(self.url_inscription)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/inscription.html')

    def test_inscription_valide(self):
        """Vérifie qu'un utilisateur peut s'inscrire avec des données valides."""
        data = {
            'prenom': 'Alice',
            'nom': 'Dupont',
            'email': 'alice@example.com',
            'username': 'alice_dupont',
            'telephone': '+221771234567',
            'mot_de_passe': 'MotDePasse123!',
            'confirmer_mot_de_passe': 'MotDePasse123!',
        }
        response = self.client.post(self.url_inscription, data)
        # Doit rediriger vers le dashboard après inscription
        self.assertEqual(response.status_code, 302)
        # L'utilisateur doit exister en base
        self.assertTrue(User.objects.filter(email='alice@example.com').exists())

    def test_inscription_email_duplique(self):
        """Vérifie qu'on ne peut pas s'inscrire avec un email déjà utilisé."""
        # Créer un utilisateur existant
        User.objects.create_user(
            username='existant',
            email='existant@example.com',
            password='Test1234!',
            prenom='Jean',
            nom='Test'
        )
        data = {
            'prenom': 'Bob',
            'nom': 'Martin',
            'email': 'existant@example.com',  # Email déjà utilisé
            'username': 'bob_martin',
            'mot_de_passe': 'MotDePasse123!',
            'confirmer_mot_de_passe': 'MotDePasse123!',
        }
        response = self.client.post(self.url_inscription, data)
        # Doit rester sur la page d'inscription (formulaire invalide)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'déjà associée')

    def test_inscription_mots_de_passe_differents(self):
        """Vérifie la validation de la confirmation du mot de passe."""
        data = {
            'prenom': 'Alice',
            'nom': 'Dupont',
            'email': 'alice2@example.com',
            'username': 'alice_dupont2',
            'mot_de_passe': 'MotDePasse123!',
            'confirmer_mot_de_passe': 'AutreMot456!',  # Différent
        }
        response = self.client.post(self.url_inscription, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ne correspondent pas')


class ConnexionTestCase(TestCase):
    """Tests du processus de connexion."""

    def setUp(self):
        """Créer un utilisateur de test."""
        self.client = Client()
        self.url_connexion = reverse('accounts:connexion')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='MotDePasse123!',
            prenom='Test',
            nom='Utilisateur'
        )

    def test_connexion_valide(self):
        """Vérifie la connexion avec des identifiants corrects."""
        response = self.client.post(self.url_connexion, {
            'username': 'test@example.com',
            'password': 'MotDePasse123!',
        })
        # Redirection après connexion réussie
        self.assertEqual(response.status_code, 302)

    def test_connexion_invalide(self):
        """Vérifie le rejet des mauvais identifiants."""
        response = self.client.post(self.url_connexion, {
            'username': 'test@example.com',
            'password': 'mauvais_mot_de_passe',
        })
        self.assertEqual(response.status_code, 200)

    def test_deconnexion(self):
        """Vérifie la déconnexion."""
        self.client.login(username='test@example.com', password='MotDePasse123!')
        response = self.client.get(reverse('accounts:deconnexion'))
        self.assertEqual(response.status_code, 302)


class UserModelTestCase(TestCase):
    """Tests du modèle User."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='modeltest',
            email='model@example.com',
            password='Test1234!',
            prenom='Marie',
            nom='Curie'
        )

    def test_get_full_name(self):
        """Vérifie la méthode get_full_name."""
        self.assertEqual(self.user.get_full_name(), 'Marie Curie')

    def test_str_representation(self):
        """Vérifie la représentation en chaîne."""
        self.assertIn('Marie', str(self.user))
        self.assertIn('Curie', str(self.user))
