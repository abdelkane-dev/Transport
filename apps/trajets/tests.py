"""
Tests de l'application Trajets.
Couvre : modèle Trajet, validation bus actif, vues CRUD.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from apps.bus.models import Bus
from .models import Trajet

User = get_user_model()


class TrajetModelTestCase(TestCase):
    """Tests du modèle Trajet."""

    def setUp(self):
        """Créer des objets de test."""
        self.bus_actif = Bus.objects.create(
            immatriculation='DK-ACT-01',
            nombre_places=50,
            statut='ACTIF'
        )
        self.bus_inactif = Bus.objects.create(
            immatriculation='DK-INA-01',
            nombre_places=30,
            statut='INACTIF'
        )
        self.demain = date.today() + timedelta(days=1)

        self.trajet = Trajet.objects.create(
            ville_depart='Dakar',
            ville_arrivee='Thiès',
            date_depart=self.demain,
            heure_depart='08:00',
            prix=5000,
            bus=self.bus_actif
        )

    def test_creation_trajet_valide(self):
        """Vérifie qu'un trajet peut être créé avec un bus actif."""
        self.assertEqual(self.trajet.ville_depart, 'Dakar')
        self.assertEqual(self.trajet.ville_arrivee, 'Thiès')
        self.assertEqual(self.trajet.bus, self.bus_actif)

    def test_bus_inactif_rejete(self):
        """Vérifie qu'un bus inactif ne peut pas être assigné à un trajet."""
        trajet = Trajet(
            ville_depart='Dakar',
            ville_arrivee='Kaolack',
            date_depart=self.demain,
            heure_depart='10:00',
            prix=8000,
            bus=self.bus_inactif  # Bus inactif → doit échouer
        )
        with self.assertRaises(ValidationError) as ctx:
            trajet.full_clean()
        self.assertIn('ACTIF', str(ctx.exception))

    def test_meme_ville_depart_arrivee_rejete(self):
        """Vérifie qu'on ne peut pas avoir la même ville de départ et d'arrivée."""
        trajet = Trajet(
            ville_depart='Dakar',
            ville_arrivee='Dakar',  # Même ville !
            date_depart=self.demain,
            heure_depart='09:00',
            prix=1000,
            bus=self.bus_actif
        )
        with self.assertRaises(ValidationError):
            trajet.full_clean()

    def test_places_disponibles_sans_reservations(self):
        """Vérifie les places disponibles sans réservation."""
        self.assertEqual(self.trajet.get_places_disponibles(), 50)
        self.assertFalse(self.trajet.est_complet())

    def test_est_passe(self):
        """Vérifie la détection d'un trajet passé."""
        self.assertFalse(self.trajet.est_passe())  # Trajet demain → pas passé

        # Créer un trajet dans le passé
        hier = date.today() - timedelta(days=1)
        trajet_passe = Trajet(
            ville_depart='Dakar',
            ville_arrivee='Saint-Louis',
            date_depart=hier,
            heure_depart='06:00',
            prix=12000,
            bus=self.bus_actif
        )
        self.assertTrue(trajet_passe.est_passe())

    def test_str_representation(self):
        """Vérifie la représentation en chaîne."""
        repr_str = str(self.trajet)
        self.assertIn('Dakar', repr_str)
        self.assertIn('Thiès', repr_str)


class TrajetViewTestCase(TestCase):
    """Tests des vues de l'application Trajets."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@test.com',
            password='Admin1234!', prenom='Admin', nom='Test'
        )
        self.bus = Bus.objects.create(
            immatriculation='DK-VIEW-01', nombre_places=40, statut='ACTIF'
        )
        self.demain = date.today() + timedelta(days=1)
        self.trajet = Trajet.objects.create(
            ville_depart='Dakar', ville_arrivee='Mbour',
            date_depart=self.demain, heure_depart='07:00',
            prix=3000, bus=self.bus
        )

    def test_liste_trajets_accessible(self):
        """La liste des trajets est accessible sans connexion."""
        response = self.client.get(reverse('trajets:liste'))
        self.assertEqual(response.status_code, 200)

    def test_detail_trajet(self):
        """Le détail d'un trajet est accessible."""
        response = self.client.get(reverse('trajets:detail', kwargs={'pk': self.trajet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dakar')

    def test_creer_trajet_admin_seulement(self):
        """Seul un admin peut créer un trajet."""
        self.client.login(username='admin@test.com', password='Admin1234!')
        response = self.client.post(reverse('trajets:creer'), {
            'ville_depart': 'Dakar',
            'ville_arrivee': 'Ziguinchor',
            'date_depart': str(self.demain),
            'heure_depart': '08:00',
            'prix': '15000',
            'bus': self.bus.pk,
        })
        self.assertEqual(response.status_code, 302)  # Redirection = succès
