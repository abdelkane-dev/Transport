"""
Tests de l'application Bus.
Couvre : modèle Bus, vues CRUD, validations.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Bus

User = get_user_model()


class BusModelTestCase(TestCase):
    """Tests du modèle Bus."""

    def setUp(self):
        """Créer un bus de test."""
        self.bus = Bus.objects.create(
            immatriculation='DK-0001-TEST',
            nombre_places=50,
            statut='ACTIF'
        )

    def test_creation_bus(self):
        """Vérifie la création d'un bus."""
        self.assertEqual(self.bus.immatriculation, 'DK-0001-TEST')
        self.assertEqual(self.bus.nombre_places, 50)
        self.assertEqual(self.bus.statut, 'ACTIF')

    def test_str_representation(self):
        """Vérifie la représentation en chaîne."""
        self.assertIn('DK-0001-TEST', str(self.bus))
        self.assertIn('50', str(self.bus))

    def test_est_actif(self):
        """Vérifie la méthode est_actif."""
        self.assertTrue(self.bus.est_actif())
        self.bus.statut = 'INACTIF'
        self.assertFalse(self.bus.est_actif())

    def test_immatriculation_unique(self):
        """Vérifie que l'immatriculation est unique."""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Bus.objects.create(
                immatriculation='DK-0001-TEST',  # Dupliqué
                nombre_places=30,
                statut='ACTIF'
            )


class BusViewTestCase(TestCase):
    """Tests des vues de l'application Bus."""

    def setUp(self):
        """Créer des utilisateurs et bus de test."""
        self.client = Client()

        # Utilisateur admin
        self.admin = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='Admin1234!',
            prenom='Admin',
            nom='Test'
        )

        # Utilisateur normal
        self.user = User.objects.create_user(
            username='user_test',
            email='user@test.com',
            password='User1234!',
            prenom='User',
            nom='Test'
        )

        # Bus de test
        self.bus = Bus.objects.create(
            immatriculation='DK-TEST-01',
            nombre_places=40,
            statut='ACTIF'
        )

    def test_liste_bus_accessible(self):
        """La liste des bus est accessible sans connexion."""
        response = self.client.get(reverse('bus:liste'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bus/bus_liste.html')

    def test_creer_bus_admin_seulement(self):
        """Seul un admin peut créer un bus."""
        # Sans connexion → redirection ou refus
        response = self.client.post(reverse('bus:creer'), {
            'immatriculation': 'DK-NEW-01',
            'nombre_places': 30,
            'statut': 'ACTIF',
        })
        self.assertNotEqual(response.status_code, 200)  # Pas d'accès

        # Avec connexion admin → succès
        self.client.login(username='admin@test.com', password='Admin1234!')
        response = self.client.post(reverse('bus:creer'), {
            'immatriculation': 'DK-NEW-01',
            'nombre_places': 30,
            'statut': 'ACTIF',
        })
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertTrue(Bus.objects.filter(immatriculation='DK-NEW-01').exists())

    def test_filtrage_par_statut(self):
        """Le filtre par statut fonctionne correctement."""
        Bus.objects.create(immatriculation='BUS-INACTIF', nombre_places=20, statut='INACTIF')
        response = self.client.get(reverse('bus:liste') + '?statut=ACTIF')
        self.assertEqual(response.status_code, 200)
        # Vérifier que le bus inactif n'est pas dans les résultats
        for bus in response.context['bus_list']:
            self.assertEqual(bus.statut, 'ACTIF')
