"""
Tests de l'application Réservations.
Couvre : création, annulation, validation des places, isolation par client.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from apps.bus.models import Bus
from apps.trajets.models import Trajet
from .models import Reservation

User = get_user_model()


class ReservationModelTestCase(TestCase):
    """Tests du modèle Reservation."""

    def setUp(self):
        """Préparer le contexte de test."""
        # Bus actif
        self.bus = Bus.objects.create(
            immatriculation='DK-TEST-RES', nombre_places=10, statut='ACTIF'
        )
        # Trajet futur
        self.demain = date.today() + timedelta(days=1)
        self.trajet = Trajet.objects.create(
            ville_depart='Dakar', ville_arrivee='Thiès',
            date_depart=self.demain, heure_depart='08:00',
            prix=5000, bus=self.bus
        )
        # Client de test
        self.client_user = User.objects.create_user(
            username='client_test', email='client@test.com',
            password='Test1234!', prenom='Alice', nom='Dupont'
        )

    def test_creation_reservation_valide(self):
        """Vérifie la création d'une réservation valide."""
        reservation = Reservation.objects.create(
            client=self.client_user,
            trajet=self.trajet,
            nombre_places=3
        )
        self.assertEqual(reservation.statut, 'EN_ATTENTE')
        self.assertEqual(reservation.nombre_places, 3)
        self.assertEqual(reservation.get_prix_total(), 15000)

    def test_depassement_places_rejete(self):
        """Vérifie que la réservation échoue si pas assez de places."""
        # Remplir presque le bus
        Reservation.objects.create(
            client=self.client_user, trajet=self.trajet, nombre_places=9
        )
        # Tenter de réserver 5 places alors qu'il n'en reste que 1
        reservation = Reservation(
            client=self.client_user, trajet=self.trajet, nombre_places=5
        )
        with self.assertRaises(ValidationError) as ctx:
            reservation.full_clean()
        self.assertIn('places disponibles', str(ctx.exception))

    def test_annulation_possible(self):
        """Vérifie qu'on peut annuler une réservation active sur un trajet futur."""
        reservation = Reservation.objects.create(
            client=self.client_user, trajet=self.trajet, nombre_places=2
        )
        self.assertTrue(reservation.peut_etre_annulee())
        succes, message = reservation.annuler(raison="Changement de plan")
        self.assertTrue(succes)
        self.assertEqual(reservation.statut, 'ANNULEE')

    def test_annulation_trajet_passe_impossible(self):
        """Vérifie qu'on ne peut pas annuler un trajet déjà passé."""
        hier = date.today() - timedelta(days=1)
        trajet_passe = Trajet.objects.create(
            ville_depart='Dakar', ville_arrivee='Mbour',
            date_depart=hier, heure_depart='07:00',
            prix=3000, bus=self.bus
        )
        reservation = Reservation(
            client=self.client_user, trajet=trajet_passe,
            nombre_places=1, statut='CONFIRMEE'
        )
        reservation.save()  # Sauvegarder sans full_clean pour simuler une résa existante

        succes, message = reservation.annuler()
        self.assertFalse(succes)
        self.assertIn('passé', message)

    def test_confirmation_reservation(self):
        """Vérifie la confirmation d'une réservation EN_ATTENTE."""
        reservation = Reservation.objects.create(
            client=self.client_user, trajet=self.trajet, nombre_places=1
        )
        self.assertEqual(reservation.statut, 'EN_ATTENTE')
        succes, message = reservation.confirmer()
        self.assertTrue(succes)
        self.assertEqual(reservation.statut, 'CONFIRMEE')

    def test_prix_total(self):
        """Vérifie le calcul du prix total."""
        reservation = Reservation.objects.create(
            client=self.client_user, trajet=self.trajet, nombre_places=4
        )
        # Prix = 4 places × 5000 FCFA = 20000 FCFA
        self.assertEqual(reservation.get_prix_total(), 20000)


class ReservationViewTestCase(TestCase):
    """Tests des vues de l'application Réservations."""

    def setUp(self):
        self.client_http = Client()
        self.bus = Bus.objects.create(
            immatriculation='DK-VIEW-RES', nombre_places=20, statut='ACTIF'
        )
        self.demain = date.today() + timedelta(days=1)
        self.trajet = Trajet.objects.create(
            ville_depart='Dakar', ville_arrivee='Saint-Louis',
            date_depart=self.demain, heure_depart='06:00',
            prix=12000, bus=self.bus
        )
        self.user1 = User.objects.create_user(
            username='user1', email='user1@test.com',
            password='Test1234!', prenom='Bob', nom='Martin'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@test.com',
            password='Test1234!', prenom='Charlie', nom='Brown'
        )

    def test_dashboard_requiert_connexion(self):
        """Le dashboard redirige les non-connectés."""
        response = self.client_http.get(reverse('reservations:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirection vers connexion

    def test_client_ne_voit_que_ses_reservations(self):
        """Vérifie l'isolation des réservations par client."""
        # Réservation de user1
        resa1 = Reservation.objects.create(
            client=self.user1, trajet=self.trajet, nombre_places=2
        )
        # Réservation de user2
        resa2 = Reservation.objects.create(
            client=self.user2, trajet=self.trajet, nombre_places=1
        )

        # user1 se connecte et accède au dashboard
        self.client_http.login(username='user1@test.com', password='Test1234!')
        response = self.client_http.get(reverse('reservations:dashboard'))
        self.assertEqual(response.status_code, 200)

        # user1 ne doit voir que sa réservation
        reservations = response.context['reservations']
        self.assertIn(resa1, reservations)
        self.assertNotIn(resa2, reservations)

    def test_acces_reservation_autre_client_interdit(self):
        """Vérifie qu'un client ne peut pas voir la réservation d'un autre."""
        resa_user2 = Reservation.objects.create(
            client=self.user2, trajet=self.trajet, nombre_places=1
        )
        # user1 tente d'accéder à la réservation de user2
        self.client_http.login(username='user1@test.com', password='Test1234!')
        response = self.client_http.get(
            reverse('reservations:detail', kwargs={'pk': resa_user2.pk})
        )
        # Doit être redirigé (accès refusé)
        self.assertEqual(response.status_code, 302)
