# Transport Réservation – Backend Django Complet

> Projet académique – Application de réservation de billets de bus  
> **Lead Développeur Backend :** Abdoul_Karim_Traoré | Stack : Django 5.x + DRF + SQLite

---

##  1. Description du projet

**Transport Réservation** est une application web Django permettant à une compagnie de transport de gérer sa flotte de bus, ses trajets et les réservations de ses clients.

### Objectifs
- Permettre aux clients de s'inscrire, se connecter et réserver des places de bus en ligne
- Offrir aux administrateurs un panneau complet pour gérer les bus, trajets et réservations
- Exposer une **API REST** (Django REST Framework) pour l'intégration avec des applications mobiles ou frontend JavaScript

### Ce que fait l'application
- ✅ Gestion de la flotte de bus (CRUD complet)
- ✅ Planification et gestion des trajets
- ✅ Inscription / Connexion / Déconnexion des clients
- ✅ Réservation de places avec vérification de disponibilité en temps réel
- ✅ Annulation de réservations (avec règles métier)
- ✅ Interface d'administration Django enrichie
- ✅ API REST documentée via DRF Browsable API

---

## 2. Équipe et répartition des rôles

| Rôle | Responsabilités |
|------|----------------|
| **Abdou_Karim8Traoré – Lead Backend** | Architecture Django, modèles, API REST, admin, logique métier, déploiement |
| **Oumou_Sarr_Keita – Frontend** | Templates HTML/CSS, intégration Bootstrap, UX/UI, formulaires |
| **Adama_Bengaly – Tests & DevOps** | Tests unitaires, fixtures, CI/CD, documentation technique |

> Ce dépôt contient **le travail de Abdoul_Karim_Traoré (Lead Backend)** dans son intégralité.

---

## 3. Architecture technique

### Stack technique
| Composant | Technologie |
|-----------|------------|
| Framework web | **Django 5.1.4** |
| API REST | **Django REST Framework 3.15** |
| Base de données | **SQLite** (dev) / PostgreSQL (prod) |
| Frontend | **Bootstrap 5.3** + Bootstrap Icons |
| Authentification | Django Auth + DRF Token Auth |
| Serveur dev | `python manage.py runserver` |
| Serveur prod | Gunicorn + Whitenoise |

### Structure des applications
```
transport_project/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── transport_project/       ← Configuration centrale Django
│   ├── settings.py          ← Paramètres (BDD, apps, auth, DRF...)
│   ├── urls.py              ← Routage principal (web + API)
│   └── wsgi.py              ← Point d'entrée WSGI (production)
├── apps/
│   ├── accounts/            ← Gestion des comptes utilisateurs
│   ├── bus/                 ← Gestion de la flotte de bus
│   ├── trajets/             ← Gestion des trajets planifiés
│   └── reservations/        ← Gestion des réservations clients
├── fixtures/
│   └── initial_data.json    ← Données de démonstration
├── templates/               ← Templates HTML globaux + par app
│   ├── base.html
│   ├── home.html
│   ├── bus/
│   ├── trajets/
│   ├── reservations/
│   └── accounts/
└── static/
    └── css/style.css        ← Styles CSS personnalisés
```

### Diagramme des relations entre modèles
```
┌─────────────┐       ┌──────────────┐       ┌─────────────────┐
│    User      │       │    Trajet    │       │   Reservation   │
│─────────────│       │──────────────│       │─────────────────│
│ id (PK)     │       │ id (PK)      │       │ id (PK)         │
│ email       │◄──────│ ville_depart │◄──────│ client (FK→User)│
│ username    │ 1:N   │ ville_arrivee│  1:N  │ trajet (FK→Traj)│
│ prenom      │       │ date_depart  │       │ nombre_places   │
│ nom         │       │ heure_depart │       │ date_reservation│
│ telephone   │       │ prix         │       │ statut          │
│ date_inscr. │       │ bus (FK→Bus) │       │ notes           │
└─────────────┘       └──────────────┘       └─────────────────┘
                              │
                       ┌──────┴───────┐
                       │     Bus      │
                       │──────────────│
                       │ id (PK)      │
                       │ immatriculat.│
                       │ nombre_places│
                       │ statut       │
                       │ notes        │
                       └──────────────┘
```

---

## 4. Installation et lancement

### Prérequis
- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Étape 1 – Cloner le dépôt
```bash
git clone https://github.com/votre-repo/transport_project.git
cd transport_project
```

### Étape 2 – Créer l'environnement virtuel
```bash
# Windows
python -m venv venv

# Linux / macOS
python3 -m venv venv
```

### Étape 3 – Activer l'environnement virtuel
```bash
# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```
> Vous devriez voir `(venv)` au début de votre invite de commande.

### Étape 4 – Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 5 – Configurer les variables d'environnement
```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer le fichier .env avec vos valeurs
# (pas de modification nécessaire pour le développement local)
```

### Étape 6 – Appliquer les migrations (créer la BDD)
```bash
python manage.py makemigrations
python manage.py migrate
```
> Cela crée le fichier `db.sqlite3` avec toutes les tables.

### Étape 7 – Charger les données de démonstration
```bash
# ATTENTION : chargez d'abord les bus et trajets, PAS les users
# (les users nécessitent des mots de passe hashés valides)
# Chargez uniquement les bus et trajets via fixtures :
python manage.py loaddata fixtures/initial_data.json
```
> Note : Les utilisateurs de la fixture ont des mots de passe fictifs.
> Utilisez plutôt la commande `createsuperuser` ci-dessous.

### Étape 8 – Créer un superutilisateur
```bash
python manage.py createsuperuser
# Suivre les instructions : email, username, nom, prenom, mot de passe
```

### Étape 9 – Lancer le serveur de développement
```bash
python manage.py runserver
```
>  L'application est accessible sur : **http://127.0.0.1:8000/**

### Étape 10 – Accéder aux différentes interfaces
| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Page d'accueil |
| `http://127.0.0.1:8000/admin/` | Interface d'administration |
| `http://127.0.0.1:8000/accounts/inscription/` | Inscription |
| `http://127.0.0.1:8000/accounts/connexion/` | Connexion |
| `http://127.0.0.1:8000/trajets/` | Liste des trajets |
| `http://127.0.0.1:8000/reservations/dashboard/` | Dashboard client |
| `http://127.0.0.1:8000/api/bus/` | API Bus |
| `http://127.0.0.1:8000/api/trajets/` | API Trajets |
| `http://127.0.0.1:8000/api/reservations/` | API Réservations |

---

## 5. Structure de la base de données

### Modèle `User` (app: accounts)
| Champ | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Clé primaire auto |
| `email` | EmailField (unique) | Identifiant de connexion |
| `username` | CharField | Nom d'utilisateur unique |
| `prenom` | CharField(100) | Prénom du client |
| `nom` | CharField(100) | Nom de famille |
| `telephone` | CharField(20) | Numéro de téléphone (optionnel) |
| `date_inscription` | DateTimeField | Date d'inscription (auto) |
| `is_active` | BooleanField | Compte actif |
| `is_staff` | BooleanField | Accès administration |

### Modèle `Bus` (app: bus)
| Champ | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Clé primaire auto |
| `immatriculation` | CharField(20, unique) | N° d'immatriculation |
| `nombre_places` | PositiveIntegerField | Capacité (min: 1) |
| `statut` | CharField choices | ACTIF / INACTIF / MAINTENANCE |
| `notes` | TextField | Remarques internes |
| `date_creation` | DateTimeField | Ajout automatique |
| `date_modification` | DateTimeField | Modification automatique |

### Modèle `Trajet` (app: trajets)
| Champ | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Clé primaire auto |
| `ville_depart` | CharField(100) | Ville de départ |
| `ville_arrivee` | CharField(100) | Ville d'arrivée |
| `date_depart` | DateField | Date du voyage |
| `heure_depart` | TimeField | Heure du voyage |
| `prix` | DecimalField(10,2) | Prix par place en FCFA |
| `bus` | ForeignKey(Bus) | Bus assigné (PROTECT) |
| `date_creation` | DateTimeField | Auto |

### Modèle `Reservation` (app: reservations)
| Champ | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Clé primaire auto |
| `client` | ForeignKey(User) | Client qui réserve (CASCADE) |
| `trajet` | ForeignKey(Trajet) | Trajet réservé (PROTECT) |
| `nombre_places` | PositiveIntegerField | Nb de places (min: 1) |
| `date_reservation` | DateTimeField | Date auto (auto_now_add) |
| `statut` | CharField choices | EN_ATTENTE / CONFIRMEE / ANNULEE |
| `notes` | TextField | Commentaires / raison annulation |

---

## 6. Fonctionnalités implémentées

### App `accounts` – Gestion des comptes
- ✅ Modèle User personnalisé (AbstractUser) avec champs métier
- ✅ Inscription avec validation complète (email unique, mdp confirmé)
- ✅ Connexion par email (USERNAME_FIELD = 'email')
- ✅ Déconnexion avec message de confirmation
- ✅ Vue de modification du profil (LoginRequiredMixin)
- ✅ API REST : inscription, connexion (token), déconnexion, profil
- ✅ Admin Django personnalisé avec badge réservations

### App `bus` – Gestion de la flotte
- ✅ CRUD complet des bus (Créer, Lire, Modifier, Supprimer)
- ✅ Filtre par statut (ACTIF, INACTIF, MAINTENANCE)
- ✅ Protection suppression si trajets liés
- ✅ Actions admin (marquer ACTIF/INACTIF/MAINTENANCE en lot)
- ✅ API REST avec action `/api/bus/actifs/`
- ✅ Restriction vues admin aux `is_staff` (AdminRequiredMixin)
- ✅ Pagination (10 par page)

### App `trajets` – Gestion des trajets
- ✅ CRUD complet des trajets
- ✅ Validation : bus ACTIF obligatoire (dans `clean()` du modèle)
- ✅ Validation : villes de départ ≠ arrivée
- ✅ Validation : date dans le futur (pour création)
- ✅ Recherche multi-critères (ville départ, arrivée, date)
- ✅ Calcul temps réel : places disponibles, taux de remplissage
- ✅ Méthodes `est_complet()`, `est_passe()`, `get_taux_remplissage()`
- ✅ Vue admin avec date_hierarchy et filtres avancés
- ✅ API REST avec action `/api/trajets/disponibles/`

### App `reservations` – Gestion des réservations
- ✅ Réservation en 2 étapes (détail trajet → formulaire → confirmation)
- ✅ Validation des places disponibles (avec exclusion des annulées)
- ✅ Isolation par client (un client ne voit QUE ses réservations)
- ✅ Méthode `peut_etre_annulee()` avec règle trajet non passé
- ✅ Annulation avec raison optionnelle
- ✅ Confirmation par les administrateurs
- ✅ Dashboard client avec statistiques
- ✅ Vue admin : toutes les réservations avec filtres
- ✅ API REST avec actions `/annuler/` et `/confirmer/`
- ✅ Calcul du prix total (`get_prix_total()`)

---

## 7. Tester l'application

### Scénario 1 : Inscription et connexion
```
1. Aller sur http://127.0.0.1:8000/accounts/inscription/
2. Remplir : Prénom, Nom, Email, Username, Téléphone, Mot de passe
3. Cliquer "Créer mon compte" → redirection vers le dashboard
4. Se déconnecter puis se reconnecter sur /accounts/connexion/
```

### Scénario 2 : Créer un bus (admin)
```
1. Se connecter avec le compte superutilisateur
2. Aller sur http://127.0.0.1:8000/bus/creer/
3. Remplir : Immatriculation (ex: DK-TEST-01), Nb places (50), Statut ACTIF
4. Cliquer "Ajouter" → le bus apparaît dans la liste
5. Tester le filtre par statut
```

### Scénario 3 : Créer un trajet (admin)
```
1. Aller sur http://127.0.0.1:8000/trajets/creer/
2. Remplir : Dakar → Thiès, demain, 08:00, 5000 FCFA, bus DK-TEST-01
3. Tenter avec un bus INACTIF → erreur métier attendue
4. Valider avec un bus ACTIF → trajet créé
```

### Scénario 4 : Réserver une place (client)
```
1. Se connecter en tant que client (pas admin)
2. Aller sur http://127.0.0.1:8000/trajets/
3. Cliquer sur un trajet disponible → "Réserver"
4. Choisir 2 places → voir le prix total se calculer
5. Confirmer → réservation créée en statut "En attente"
6. Voir la réservation dans le dashboard
```

### Scénario 5 : Annuler une réservation
```
1. Dans le dashboard, cliquer sur l'icône ❌ d'une réservation
2. Saisir une raison (optionnel)
3. Confirmer → statut passe à "Annulée"
4. Les places sont libérées et disponibles à nouveau
```

### Scénario 6 : Tester l'API REST
```bash
# Liste des bus
curl http://127.0.0.1:8000/api/bus/

# Créer un compte
curl -X POST http://127.0.0.1:8000/api/accounts/inscription/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","prenom":"Test","nom":"User","mot_de_passe":"Test1234!","confirmer_mot_de_passe":"Test1234!"}'

# Se connecter et obtenir un token
curl -X POST http://127.0.0.1:8000/api/accounts/connexion/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test1234!"}'

# Utiliser le token pour accéder aux réservations
curl http://127.0.0.1:8000/api/reservations/ \
  -H "Authorization: Token VOTRE_TOKEN_ICI"
```

### Lancer tous les tests unitaires
```bash
# Tous les tests
python manage.py test

# Tests d'une app spécifique
python manage.py test apps.accounts
python manage.py test apps.bus
python manage.py test apps.trajets
python manage.py test apps.reservations

# Avec verbosité
python manage.py test --verbosity=2
```

---

## 8. Bugs connus / Limitations

| # | Description | Statut |
|---|-------------|--------|
| 1 | Les fixtures `initial_data.json` ont des mots de passe fictifs – les users ne peuvent pas se connecter via les fixtures | Connu – utiliser `createsuperuser` |
| 2 | Pas de système de pagination sur la vue admin des réservations | Limitation intentionnelle |
| 3 | La suppression d'un bus avec trajets passés (et réservations annulées) est bloquée | Comportement conservateur intentionnel |
| 4 | Pas de système de notification email implémenté | Hors périmètre (prévu v2) |
| 5 | Pas de système de paiement | Hors périmètre explicite |
| 6 | L'API ne renvoie pas de token JWT (utilise Token simple DRF) | Simple d'implémentation, JWT prévu v2 |

---

## 9. Commandes utiles

### Gestion de la base de données
```bash
# Créer les fichiers de migration après modification des modèles
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Voir le SQL généré par une migration
python manage.py sqlmigrate bus 0001

# Afficher l'état des migrations
python manage.py showmigrations

# Réinitialiser la BDD (ATTENTION : perte de données)
rm db.sqlite3 && python manage.py migrate
```

### Gestion des utilisateurs
```bash
# Créer un superutilisateur interactif
python manage.py createsuperuser

# Changer un mot de passe
python manage.py changepassword <username>
```

### Shell Django (debug et exploration)
```bash
# Ouvrir le shell interactif
python manage.py shell

# Exemples dans le shell :
# from apps.bus.models import Bus
# Bus.objects.all()
# Bus.objects.filter(statut='ACTIF').count()
# from apps.reservations.models import Reservation
# Reservation.objects.filter(client__email='test@test.com')
```

### Fichiers statiques
```bash
# Collecter les fichiers statiques pour la production
python manage.py collectstatic

# Effacer sans confirmation
python manage.py collectstatic --noinput
```

### Chargement des fixtures
```bash
# Charger les données initiales (bus et trajets)
python manage.py loaddata fixtures/initial_data.json

# Exporter les données actuelles en fixture
python manage.py dumpdata --indent 2 > fixtures/backup.json

# Exporter une app spécifique
python manage.py dumpdata apps.bus --indent 2 > fixtures/bus_backup.json
```

### Vérification du projet
```bash
# Vérifier les problèmes de configuration
python manage.py check

# Vérifier les problèmes de déploiement
python manage.py check --deploy
```

---

## 10. Planning et livrables

### Ce qui a été livré (Version 1.0)
| Livrable | Statut | Date |
|----------|--------|------|
| Modèle User personnalisé | ✅ Livré | Sprint 1 |
| Authentification complète | ✅ Livré | Sprint 1 |
| Modèle Bus + CRUD | ✅ Livré | Sprint 2 |
| Modèle Trajet + CRUD + validations | ✅ Livré | Sprint 2 |
| Modèle Réservation + logique métier | ✅ Livré | Sprint 3 |
| Annulation avec règles | ✅ Livré | Sprint 3 |
| Admin Django personnalisé (4 apps) | ✅ Livré | Sprint 3 |
| API REST DRF (4 apps) | ✅ Livré | Sprint 4 |
| Templates HTML complets | ✅ Livré | Sprint 4 |
| Tests unitaires | ✅ Livré | Sprint 4 |
| Fixtures de démonstration | ✅ Livré | Sprint 4 |
| Documentation README | ✅ Livré | Sprint 4 |

### Prévu pour Version 2.0
- [ ] Notifications email (confirmation, annulation)
- [ ] JWT Authentication (via `djangorestframework-simplejwt`)
- [ ] Système de codes de réservation (QR code ou PDF)
- [ ] Statistiques avancées pour les administrateurs
- [ ] Déploiement sur serveur (Railway, Render, ou VPS)

---

## Décisions techniques expliquées

### Pourquoi `AbstractUser` et pas `AbstractBaseUser` ?
`AbstractUser` garde tous les champs Django par défaut (username, email, groups, permissions) et nous permet d'en ajouter sans réécrire l'authentification. C'est la solution recommandée pour les projets où on veut personnaliser sans repartir de zéro.

### Pourquoi `on_delete=PROTECT` sur les ForeignKeys ?
Pour les trajets→bus et réservations→trajet, nous utilisons `PROTECT` au lieu de `CASCADE`. Cela **empêche la suppression accidentelle** d'un bus ou trajet qui a encore des données liées, ce qui évite les corruptions de données.

### Pourquoi `clean()` dans le modèle Trajet et Réservation ?
La validation métier dans `clean()` s'assure que les règles sont vérifiées **indépendamment de l'interface utilisée** (formulaire HTML, API REST, Django Admin, shell). Si on mettait la validation uniquement dans les formulaires, l'API pourrait contourner ces règles.

### Pourquoi CBV (Class-Based Views) ?
Les CBV permettent de réutiliser le comportement commun via `LoginRequiredMixin`, `UserPassesTestMixin`, etc. Elles sont plus maintenables pour des projets de taille moyenne et suivent les conventions Django.
