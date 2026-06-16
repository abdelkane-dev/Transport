# 🚌 Application de Réservation de Billets – Transport

## 📋 Description

Cette application web permet à une compagnie de transport de gérer efficacement :

- Les bus de sa flotte
- Les trajets disponibles
- Les réservations des voyageurs
- L'authentification des utilisateurs
- L'administration complète de la plateforme

L'objectif est de fournir une solution moderne, simple et sécurisée pour la réservation de billets de transport en ligne.

---

## ✨ Fonctionnalités principales

### 👤 Utilisateurs

- Création de compte
- Connexion / Déconnexion
- Consultation des trajets disponibles
- Recherche multicritère
- Réservation de billets
- Consultation de l'historique des réservations
- Annulation d'une réservation

### 🛠️ Administrateurs

- Gestion des bus (CRUD)
- Gestion des trajets (CRUD)
- Gestion des réservations
- Suivi de l'activité de la plateforme

---

## 👥 Équipe Projet

| Rôle | Membre |
|--------|---------|
| Lead Backend | Personne 1 |
| Frontend & Intégration | Personne 2 |
| QA & Documentation | Personne 3 |

---

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|------------|-------------|
| Django 5.x | Framework Backend |
| SQLite | Base de données |
| Bootstrap 5 | Interface utilisateur |
| HTML5 | Structure des pages |
| CSS3 | Mise en forme |
| JavaScript | Interactions côté client |
| Git & GitHub | Gestion du code source |

---

## 📂 Structure du projet
transport_project/
├── apps/
│   ├── accounts/
│   ├── bus/
│   ├── trajets/
│   └── reservations/
│
├── templates/
│
├── static/
│
├── fixtures/
│
├── README.md
├── GUIDE_UTILISATEUR.md
├── GUIDE_ADMIN.md
├── RAPPORT_TESTS.md
└── requirements.txt

---

## 🚀 Installation

### 1. Cloner le projet
git clone https://github.com/votre-organisation/transport-reservation.git
cd transport-reservation

### 2. Créer un environnement virtuel
python -m venv venv

### 3. Activer l'environnement

Linux / macOS
source venv/bin/activate

Windows
venv\Scripts\activate

### 4. Installer les dépendances
pip install -r requirements.txt

### 5. Appliquer les migrations
python manage.py migrate

### 6. Charger les données de démonstration
python manage.py loaddata fixtures/initial_data.json

### 7. Créer un administrateur
python manage.py createsuperuser

### 8. Lancer le serveur
python manage.py runserver

L'application sera accessible à l'adresse :
http://127.0.0.1:8000/

---

## 🔐 Comptes de test

| Type | Email | Mot de passe |
|--------|--------|-------------|
| Admin | admin@test.com | **** |
| Client | client@test.com | **** |

*(À adapter selon les données du projet.)*

---

## 🧪 Assurance Qualité

Les campagnes de tests sont documentées dans :
RAPPORT_TESTS.md

Les anomalies détectées sont suivies via :

- GitHub Issues
- Rapports de bugs documentés
- Captures d'écran des anomalies

---

## 📚 Documentation

- GUIDE_UTILISATEUR.md
- GUIDE_ADMIN.md
- RAPPORT_TESTS.md
- API.md

---

## 📄 Licence

Projet réalisé dans le cadre d'un projet académique de développement web.

# 👤 Guide Utilisateur
## Application de Réservation de Billets de Transport

---

# 📋 Introduction

Bienvenue sur l'application de réservation de billets de transport.

Cette plateforme vous permet de :

- Créer un compte utilisateur
- Rechercher des trajets disponibles
- Réserver des places
- Consulter vos réservations
- Annuler une réservation si nécessaire

---

# 🔐 Création d'un compte

## Étape 1 : Accéder à la page d'inscription

Depuis la page d'accueil :

- Cliquez sur le bouton S'inscrire

## Étape 2 : Remplir le formulaire

Renseignez les informations demandées :

- Nom complet
- Adresse email
- Numéro de téléphone (si demandé)
- Mot de passe
- Confirmation du mot de passe

## Étape 3 : Validation

Cliquez sur :
Créer mon compte

### Résultat attendu

- Le compte est créé avec succès.
- Vous êtes redirigé vers l'accueil ou votre espace personnel.

---

# 🔑 Connexion

## Étape 1

Cliquez sur :
Connexion

## Étape 2

Saisissez :

- Votre email
- Votre mot de passe

## Étape 3

Cliquez sur :
Se connecter

### Résultat attendu

Vous accédez à votre espace utilisateur.

---

# 🔍 Recherche d'un trajet

Depuis la page principale :

## Renseigner les critères

- Ville de départ
- Ville d'arrivée
- Date de voyage

## Lancer la recherche

Cliquez sur :
Rechercher

### Résultat attendu

La liste des trajets correspondant à votre recherche s'affiche.

---

# 🚌 Consultation d'un trajet

Pour consulter les détails :

1. Sélectionnez un trajet.
2. Cliquez sur Voir les détails.

Vous pourrez consulter :

- Horaire de départ
- Horaire d'arrivée
- Prix du billet
- Nombre de places disponibles
- Informations du bus

---

# 🎫 Réserver un billet

## Étape 1 : Choisir un trajet

Sélectionnez le trajet souhaité.

## Étape 2 : Choisir le nombre de places

Indiquez :
Nombre de places à réserver

## Étape 3 : Confirmer

Cliquez sur :
Réserver

### Résultat attendu

- La réservation est enregistrée.
- Les places disponibles sont mises à jour.
- Une confirmation apparaît à l'écran.

---

# 📑 Consulter ses réservations

Accédez au menu :
Mes réservations

Vous pouvez visualiser :

- Numéro de réservation
- Date du trajet
- Nombre de places réservées
- Montant payé
- Statut de la réservation

---

# ❌ Annuler une réservation

## Conditions

L'annulation est possible uniquement si :

- Le trajet n'a pas encore commencé.
- Les règles de la compagnie l'autorisent.

## Procédure

1. Ouvrir Mes réservations
2. Sélectionner la réservation concernée
3. Cliquer sur :
Annuler

4. Confirmer l'opération

### Résultat attendu

- La réservation est annulée.
- Les places sont remises à disposition.

---

# 👤 Modifier son profil

Depuis l'espace personnel :

1. Ouvrir Mon profil
2. Modifier les informations souhaitées
3. Enregistrer les changements

Les informations mises à jour sont immédiatement prises en compte.

---

# 🚪 Déconnexion

Pour quitter votre session :

1. Cliquer sur votre profil
2. Sélectionner :
Déconnexion

### Résultat attendu

Vous êtes redirigé vers la page d'accueil.

---

# ⚠️ Messages d'erreur courants

## Email déjà utilisé
Cette adresse email est déjà enregistrée.

## Mot de passe incorrect
Identifiants invalides.

## Places insuffisantes
Le nombre de places demandé dépasse les places disponibles.

## Champs obligatoires
Veuillez remplir tous les champs requis.

---

# 📞 Assistance

En cas de problème :

- Contactez l'administrateur de la plateforme
- Signalez le problème via le formulaire de contact
- Fournissez une capture d'écran si possible

---

# Merci d'utiliser notre plateforme de réservation 🚍

# 🛠️ Guide Administrateur
## Application de Réservation de Billets de Transport

---

# 📋 Introduction

Ce guide est destiné aux administrateurs de la plateforme.

L'administrateur dispose des privilèges nécessaires pour :

- Gérer les bus
- Gérer les trajets
- Consulter les réservations
- Superviser l'activité de l'application
- Assurer la disponibilité des services proposés aux utilisateurs

---

# 🔐 Connexion à l'espace administrateur

## Étape 1

Accéder à la page :
/admin

ou
Connexion Administrateur

## Étape 2

Saisir :

- Adresse email administrateur
- Mot de passe

## Étape 3

Cliquer sur :
Se connecter

### Résultat attendu

Accès au tableau de bord administrateur.

---

# 📊 Tableau de bord

Le tableau de bord permet de visualiser rapidement :

- Nombre total de bus
- Nombre total de trajets
- Nombre total de réservations
- Activité récente
- Statistiques générales

---

# 🚌 Gestion des Bus

## Liste des bus

Menu :
Administration → Bus

L'administrateur peut consulter :

- Numéro du bus
- Capacité
- Statut
- Date de création

---

# ➕ Ajouter un bus

## Étapes

1. Cliquer sur :
Ajouter un bus

2. Renseigner :

- Numéro du bus
- Capacité
- Description (optionnel)

3. Valider

### Résultat attendu

Le bus est enregistré dans la base de données.

---

# ✏️ Modifier un bus

## Étapes

1. Sélectionner un bus
2. Cliquer sur :
Modifier

3. Mettre à jour les informations
4. Enregistrer

### Résultat attendu

Les modifications sont immédiatement visibles.

---

# ❌ Supprimer un bus

## Étapes

1. Sélectionner un bus
2. Cliquer sur :
Supprimer

3. Confirmer l'action

### Résultat attendu

Le bus est supprimé.

---

# 🟢 Gestion du statut d'un bus

Chaque bus possède un statut :

| Statut | Description |
|----------|-------------|
| Actif | Disponible pour les trajets |
| Inactif | Temporairement indisponible |
| Maintenance | En réparation ou contrôle |

### Important

Un trajet ne peut être associé qu'à un bus actif.

---

# 🛣️ Gestion des Trajets

Menu :
Administration → Trajets

---

# ➕ Ajouter un trajet

## Informations requises

- Ville de départ
- Ville d'arrivée
- Date
- Heure
- Prix
- Bus assigné

### Validation

Le système vérifie que :

- Le bus est actif
- Les informations sont complètes

---

# ✏️ Modifier un trajet

1. Sélectionner un trajet
2. Cliquer sur :
Modifier

3. Mettre à jour les données
4. Enregistrer

### Résultat attendu

Le trajet est mis à jour.

---

# ❌ Supprimer un trajet

1. Sélectionner un trajet
2. Cliquer sur :
Supprimer

3. Confirmer

### Résultat attendu

Le trajet est retiré du système.

---

# 🎫 Gestion des Réservations

Menu :
Administration → Réservations

L'administrateur peut :

- Consulter les réservations
- Rechercher une réservation
- Vérifier les statuts
- Contrôler les disponibilités

---

# 🔍 Recherche avancée

Les filtres disponibles peuvent inclure :

- Nom du client
- Date du trajet
- Statut
- Ville de départ
- Ville d'arrivée

---

# 👥 Gestion des Utilisateurs

Selon les fonctionnalités implémentées, l'administrateur peut :

- Consulter les comptes
- Activer ou désactiver un compte
- Réinitialiser certaines informations

---

# ⚠️ Gestion des erreurs

## Bus inactif

Message :
Impossible d'assigner un bus inactif à un trajet.

## Capacité insuffisante

Message :
La capacité du bus ne permet pas cette opération.

## Champs obligatoires

Message :
Veuillez renseigner tous les champs requis.

---

# 🔒 Bonnes pratiques

## Gestion des bus

- Vérifier régulièrement les statuts
- Désactiver les bus indisponibles

## Gestion des trajets

- Contrôler les horaires
- Vérifier les prix avant publication

## Gestion des réservations

- Surveiller les annulations
- Vérifier les anomalies de réservation

---

# 🧪 Contrôle Qualité

Avant chaque mise en production :

- Vérifier la création des trajets
- Vérifier les réservations
- Vérifier les capacités des bus
- Vérifier les droits d'accès administrateur
- Vérifier l'affichage mobile et desktop

---

# 📞 Support Technique

En cas de problème :

1. Consulter les logs système
2. Vérifier la base de données
3.
Ouvrir une Issue GitHub
4. Contacter l'équipe de développement

---

# ✅ Fin du Guide Administrateur

L'administrateur est responsable du bon fonctionnement opérationnel de la plateforme et du maintien de la cohérence des données.

# 🧪 RAPPORT DE TESTS
## Application de Réservation de Billets de Transport

---

# 📋 Informations générales

| Élément | Valeur |
|----------|---------|
| Projet | Application de Réservation de Billets |
| Version testée | v1.0 |
| Responsable QA | Personne 3 |
| Date des tests | __ / __ / __ |
| Environnement | Développement |
| Statut global | En cours |

---

# 🎯 Objectif

L'objectif de cette campagne de tests est de vérifier le bon fonctionnement de l'ensemble des fonctionnalités de l'application.

Les tests portent sur :

- Authentification
- Gestion des trajets
- Réservation
- Administration
- Responsive Design
- Validation des formulaires

---

# 📊 Résumé des résultats

| Catégorie | Nombre |
|------------|---------|
| Cas de test exécutés | 8 |
| Succès | 6 |
| Avertissements | 1 |
| Échecs | 1 |
| Bugs signalés | 2 |

---

# ✅ T01 – Test Inscription

## Objectif

Vérifier la création d'un compte utilisateur.

## Étapes

1. Accéder à la page d'inscription
2. Remplir le formulaire
3. Soumettre

## Résultat attendu

- Création du compte
- Redirection vers l'accueil

## Résultat obtenu

Conforme.

## Statut

✅ Réussi

---

# ⚠️ T02 – Email déjà utilisé

## Objectif

Vérifier qu'un utilisateur ne peut pas créer deux comptes avec le même email.

## Étapes

1. Utiliser une adresse email existante
2. Soumettre le formulaire

## Résultat attendu

Affichage d'un message d'erreur.

## Résultat obtenu

Le message apparaît correctement.

Cependant l'affichage pourrait être plus explicite.

## Statut

⚠️ Réussi avec remarque

## Ticket associé

Issue #1

---

# ✅ T03 – Test Connexion

## Objectif

Valider l'authentification.

## Étapes

1. Saisir un email valide
2. Saisir un mot de passe valide
3. Cliquer sur Connexion

## Résultat attendu

Accès à l'espace utilisateur.

## Résultat obtenu

Conforme.

## Statut

✅ Réussi

---

# ✅ T04 – Accès aux pages protégées

## Objectif

Empêcher les utilisateurs non connectés d'accéder aux ressources privées.

## Étapes

1. Ouvrir une URL protégée sans connexion

## Résultat attendu

Redirection vers la page de connexion.

## Résultat obtenu

Conforme.

## Statut

✅ Réussi

---

# ✅ T05 – Consultation des trajets

## Objectif

Vérifier l'affichage des trajets.

## Étapes

1. Ouvrir la liste des trajets

## Résultat attendu

Affichage de tous les trajets disponibles.

## Résultat obtenu

Conforme.

## Statut

✅ Réussi

---

# ❌ T06 – Réservation avec places insuffisantes

## Objectif

Vérifier la gestion des capacités.

## Étapes

1. Sélectionner un trajet
2. Demander plus de places que disponibles
3. Soumettre

## Résultat attendu

Blocage de la réservation.

## Résultat obtenu

Le système autorise parfois la soumission.

## Impact

Risque de sur-réservation.

## Statut

❌ Échec

## Ticket associé

Issue #2

---

# ✅ T07 – Gestion des Bus (CRUD)

## Objectif

Tester les opérations administratives.

## Étapes

1. Créer un bus
2. Modifier un bus
3. Supprimer un bus

## Résultat attendu

Toutes les opérations fonctionnent correctement.

## Résultat obtenu

Conforme.

## Statut

✅ Réussi

---

# ✅ T08 – Responsive Design

## Objectif

Vérifier l'affichage mobile et desktop.

## Étapes

1. Tester sur écran mobile
2. Tester sur écran desktop

## Résultat attendu

Interface lisible et cohérente.

## Résultat obtenu

Conforme.

## Statut

✅ Réussi

---

# 🐛 Synthèse des anomalies

## Bug #1

### Titre

Message d'erreur peu explicite lors de l'inscription.

### Gravité

Faible

### Priorité

Basse

### Statut

Ouvert

---

## Bug #2

### Titre

Réservation possible malgré un nombre insuffisant de places.

### Gravité

Élevée

### Priorité

Haute

### Statut

Ouvert

---

# 📈 Couverture fonctionnelle

| Module | Couverture |
|----------|-----------|
| Authentification | 100% |
| Trajets | 100% |
| Réservations | 90% |
| Administration Bus | 100% |
| Administration Trajets | 90% |
| Responsive | 100% |
| Formulaires | 90% |

---

# 🔧 Recommandations

## Priorité Haute

- Corriger la validation du nombre de places disponibles.

## Priorité Moyenne

- Ajouter davantage de validations serveur.
## Priorité Faible

- Améliorer la clarté des messages d'erreur.

---

# ✅ Conclusion

La plateforme est globalement fonctionnelle et répond aux besoins principaux du projet.

La majorité des fonctionnalités critiques sont validées.

Avant la mise en production, il est recommandé de corriger le bug critique lié à la réservation de places afin de garantir la cohérence des données et d'éviter les sur-réservations.

---

# Signature QA

Nom : __________________

Date : __________________

Validation : __________________

# 📡 Documentation API
## Application de Réservation de Billets de Transport

---

# 📋 Introduction

Cette documentation décrit les principaux endpoints de l'API utilisés par l'application.

Format des données :
Content-Type: application/json

Réponses :
{
  "success": true,
  "message": "Opération effectuée avec succès"
}

---

# 🔐 Authentification

## Inscription

### Endpoint
POST /api/auth/register/

### Corps de la requête
{
  "nom": "Mamadou Diallo",
  "email": "mamadou@email.com",
  "password": "motdepasse123",
  "confirm_password": "motdepasse123"
}

### Réponse
{
  "success": true,
  "message": "Compte créé avec succès"
}

---

## Connexion

### Endpoint
POST /api/auth/login/

### Corps de la requête
{
  "email": "mamadou@email.com",
  "password": "motdepasse123"
}

### Réponse
{
  "token": "xxxxxxxxxxxxxxxx",
  "user_id": 1
}

---

## Déconnexion

### Endpoint
POST /api/auth/logout/

### Réponse
{
  "success": true,
  "message": "Déconnexion réussie"
}

---

# 👤 Utilisateurs

## Profil utilisateur

### Endpoint
GET /api/profile/

### Réponse
{
  "id": 1,
  "nom": "Mamadou Diallo",
  "email": "mamadou@email.com"
}

---

# 🚌 Gestion des Bus

## Liste des bus

### Endpoint
GET /api/bus/

### Réponse
[
  {
    "id": 1,
    "numero": "BUS001",
    "capacite": 50,
    "statut": "Actif"
  }
]

---

## Ajouter un bus

### Endpoint
POST /api/bus/

### Corps de la requête
{
  "numero": "BUS002",
  "capacite": 60,
  "statut": "Actif"
}

---

## Modifier un bus

### Endpoint
PUT /api/bus/{id}/

### Corps de la requête
{
  "capacite": 70
}

---

## Supprimer un bus

### Endpoint
DELETE /api/bus/{id}/

---

# 🛣️ Gestion des Trajets

## Liste des trajets

### Endpoint
GET /api/trajets/

### Réponse
[
  {
    "id": 1,
    "depart": "Bamako",
    "arrivee": "Sikasso",
    "prix": 5000
  }
]

---

## Détails d'un trajet

### Endpoint
GET /api/trajets/{id}/

---

## Création d'un trajet

### Endpoint
POST /api/trajets/

### Corps de la requête
{
  "depart": "Bamako",
  "arrivee": "Kayes",
  "date_depart": "2026-06-20",
  "heure_depart": "08:00",
  "prix": 7000,
  "bus_id": 2
}

---

## Modification d'un trajet

### Endpoint
PUT /api/trajets/{id}/

---

## Suppression d'un trajet

### Endpoint
DELETE /api/trajets/{id}/

---

# 🎫 Réservations

## Liste des réservations utilisateur

### Endpoint
GET /api/reservations/

### Réponse
[
  {
    "id": 1,
    "trajet": "Bamako → Sikasso",
    "places": 2,
    "statut": "Confirmée"
  }
]

---

## Créer une réservation

### Endpoint
POST /api/reservations/

### Corps de la requête
{
  "trajet_id": 1,
  "nombre_places": 2
}

### Réponse
{
  "success": true,
  "reservation_id": 15
}

---

## Annuler une réservation

### Endpoint
DELETE /api/reservations/{id}/

### Réponse
{
  "success": true,
  "message": "Réservation annulée"
}

---

# ⚠️ Gestion des erreurs

## 400 – Requête invalide
{
  "error": "Données invalides"
}

---

## 401 – Non autorisé
{
  "error": "Authentification requise"
}

---

## 403 – Accès interdit
{
  "error": "Permission refusée"
}

---

## 404 – Ressource introuvable
{
  "error": "Ressource introuvable"
}

---

## 500 – Erreur serveur
{
  "error": "Erreur interne du serveur"
}

---

# 🔒 Sécurité

- Authentification obligatoire pour les opérations protégées.
- Validation des données côté serveur.
- Vérification des permissions administrateur.
- Protection contre les accès non autorisés.

---

# 📌 Version API

Version : v1.0

Dernière mise à jour : __ / __ / __