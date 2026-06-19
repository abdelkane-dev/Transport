# 🚌 Transport Réservation

<div align="center">

[![Django](https://img.shields.io/badge/Django-5.1.4-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![ReportLab](https://img.shields.io/badge/ReportLab-4.2.2-0078D4?style=for-the-badge)](https://www.reportlab.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-31%2F31%20✅-brightgreen?style=for-the-badge)]()
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)]()
[![Coverage](https://img.shields.io/badge/Coverage-~85%25-yellowgreen?style=for-the-badge)]()

</div>

<div align="center">

**Application de réservation de billets de bus — Projet DevOps Agile**
*Développé en 4 sprints Agile — Novembre 2024*

[📖 Guide Utilisateur](05_GUIDE_UTILISATEUR.md) •
[🔧 Guide Administrateur](06_GUIDE_ADMINISTRATEUR.md) •
[🔌 API REST](07_DOCUMENTATION_API.md) •
[📋 Changelog](08_CHANGELOG.md) •
[🤝 Contribuer](09_GUIDE_CONTRIBUTION.md) •
[🚀 Déploiement](10_PLAN_DEPLOIEMENT.md)

</div>

---

## 📑 Table des matières

1. [Vue d&#39;ensemble](#-vue-densemble)
2. [Fonctionnalités](#-fonctionnalités)
3. [Architecture](#-architecture)
4. [Stack technologique](#-stack-technologique)
5. [Prérequis](#-prérequis)
6. [Installation rapide](#-installation-rapide)
7. [Configuration](#-configuration)
8. [Lancer le projet](#-lancer-le-projet)
9. [Aperçu des endpoints API](#-aperçu-des-endpoints-api)
10. [Tests](#-tests)
11. [Structure du projet](#-structure-du-projet)
12. [Équipe &amp; sprints](#-équipe--sprints)
13. [Licence](#-licence)

---

## 🎯 Vue d'ensemble

**Transport Réservation** est une application web Django complète permettant la gestion et la réservation de billets de bus en ligne. Le projet a été développé dans le cadre d'un cours DevOps en suivant la méthodologie Agile Scrum sur 4 sprints.

### Points clés

| Indicateur          | Valeur                                      |
| ------------------- | ------------------------------------------- |
| 🏗️ Architecture   | MVT (Modèle-Vue-Template) + API REST       |
| 🔒 Authentification | Email (JWT Token + Session)                 |
| 📊 API              | Django REST Framework avec pagination       |
| 📄 PDF              | Billets générés avec QR code (ReportLab) |
| 📧 Email            | Confirmation et annulation automatiques     |
| 📦 Cache            | LocMemCache (dev) / Redis (prod)            |
| 🔍 Logging          | 3 fichiers rotatifs (5 Mo, 5 archives)      |
| ✅ Tests            | 31/31 tests réussis (0 échecs)            |

---

## ✨ Fonctionnalités

### 🏃 Sprint 1 — Base & PDF (18–19 Nov 2024)

| #   | Fonctionnalité | Description                                                                 |
| --- | --------------- | --------------------------------------------------------------------------- |
| F01 | 📄 Billet PDF   | Génération automatique de billets PDF avec QR code à chaque réservation |
| F02 | 📧 Email billet | Envoi automatique du billet par email (confirmation + annulation)           |
| F03 | 📊 Dashboard    | Dashboard client avec statistiques personnelles et historique complet       |

### 🏃 Sprint 2 — Stats & Export (19–20 Nov 2024)

| #   | Fonctionnalité | Description                                                                |
| --- | --------------- | -------------------------------------------------------------------------- |
| F04 | 📈 Statistiques | Graphiques interactifs Chart.js : dépenses mensuelles, trajets populaires |
| F05 | 📤 Export CSV   | Export des réservations en UTF-8 BOM, 12 colonnes, filename horodaté     |

### 🏃 Sprint 3 — Filtres & Annulation (20–21 Nov 2024)

| #   | Fonctionnalité           | Description                                                          |
| --- | ------------------------- | -------------------------------------------------------------------- |
| F06 | 💰 Annulation remboursée | Règle de remboursement : 100% (>24h), 50% (2–24h), 0% (<2h)        |
| F07 | 🔍 Filtres avancés       | Filtres trajets : prix min/max, créneau horaire, places disponibles |
| F08 | 🔔 Notifications          | Messages Django enrichis pour chaque action utilisateur              |

### 🏃 Sprint 4 — API & Performance (21 Nov 2024)

| #   | Fonctionnalité       | Description                                                             |
| --- | --------------------- | ----------------------------------------------------------------------- |
| F09 | 🔌 API REST complète | ViewSets, pagination, filtres,`@action` personnalisées               |
| F10 | 📝 Logging structuré | 3 RotatingFileHandlers : transport, errors, reservations                |
| F11 | ⚡ Cache Redis        | Cache des trajets disponibles (TTL=300s), invalidation automatique      |
| F12 | 🔐 RBAC               | Isolation client (voit seulement ses réservations), admin `is_staff` |

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    COUCHE PRÉSENTATION                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Templates   │  │   API REST   │  │    Admin Django      │  │
│  │  (22 HTML)   │  │  /api/v1/    │  │    /admin/           │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼─────────────────┼──────────────────────┼─────────────┘
          │                 │                      │
┌─────────▼─────────────────▼──────────────────────▼─────────────┐
│                     COUCHE LOGIQUE                              │
│  ┌───────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │  Views    │  │  ViewSets    │  │  Services (PDF, Email)   │ │
│  │  (CBV/FBV)│  │  (DRF)       │  │  Logging, Cache          │ │
│  └───────────┘  └──────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
          │                 │                      │
┌─────────▼─────────────────▼──────────────────────▼─────────────┐
│                     COUCHE DONNÉES                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Applications (Apps Django)                  │   │
│  │  ┌──────────┐ ┌────────┐ ┌────────────┐ ┌────────────┐  │   │
│  │  │ accounts │ │  bus   │ │  trajets   │ │reservations│  │   │
│  │  │  User    │ │  Bus   │ │  Trajet    │ │Reservation │  │   │
│  │  └──────────┘ └────────┘ └────────────┘ └────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │   SQLite (dev)  │  │  Redis Cache │  │  Fichiers logs     │  │
│  │  PostgreSQL (p) │  │  (prod)      │  │  (RotatingFile)    │  │
│  └─────────────────┘  └──────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Modèle de données simplifié

```
User ──────────── Reservation ──────── Trajet ──────── Bus
 │ 1              N │  1               N │  1          1 │
 │ prenom          │  nombre_places      │  ville_dep    │  immatricul.
 │ nom             │  statut             │  ville_arr    │  nombre_places
 │ email           │  date_reservation   │  date_depart  │  statut
 │ telephone       │  prix_paye          │  heure_depart │
                   │  annuler()          │  prix
                   │  get_prix_total()   │  places_dispo()
```

---

## 🛠️ Stack technologique

| Composant          | Technologie                      | Version |
| ------------------ | -------------------------------- | ------- |
| Framework web      | Django                           | 5.1.4   |
| API REST           | Django REST Framework            | 3.15.2  |
| Python             | CPython                          | 3.11+   |
| Base de données   | SQLite (dev) / PostgreSQL (prod) | —      |
| Cache              | LocMemCache (dev) / Redis (prod) | —      |
| PDF                | ReportLab                        | 4.2.2   |
| QR Code            | qrcode[pil]                      | 8.0     |
| Images             | Pillow                           | 10.4.0  |
| Variables d'env    | python-decouple                  | 3.8     |
| Fichiers statiques | Whitenoise                       | 6.7.0   |
| Serveur WSGI       | Gunicorn                         | 22.0.0  |
| CORS               | django-cors-headers              | 4.4.0   |
| Filtres DRF        | django-filter                    | 24.3    |

---

## 📋 Prérequis

Avant d'installer le projet, assurez-vous d'avoir :

- **Python 3.11+** — [Télécharger](https://www.python.org/downloads/)
- **pip** (inclus avec Python)
- **Git** — [Télécharger](https://git-scm.com/)
- **Virtualenv** (recommandé)
- **Redis** (optionnel, pour le cache en production)

```bash
# Vérifier les versions
python --version   # Python 3.11.x
pip --version      # pip 23.x
git --version      # git 2.x
```

---

## ⚡ Installation rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-org/transport-reservation.git
cd transport-reservation
```

### 2. Créer l'environnement virtuel

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec vos valeurs (voir section Configuration)
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur

```bash
python manage.py createsuperuser
# Renseigner : email, prénom, nom, mot de passe
```

### 7. Charger les données de démonstration (optionnel)

```bash
python manage.py loaddata fixtures/demo_data.json
```

### 8. Lancer le serveur de développement

```bash
python manage.py runserver
```

> 🌐 L'application est accessible sur : **http://127.0.0.1:8000/**

---

## ⚙️ Configuration

### Fichier `.env`

```ini
# ── Application ─────────────────────────────────────────────
SECRET_KEY=votre-cle-secrete-django-tres-longue-et-aleatoire
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ── Base de données (production) ─────────────────────────────
# Laisser vide pour utiliser SQLite (développement)
DATABASE_URL=postgres://user:password@localhost:5432/transport_db

# ── Email ────────────────────────────────────────────────────
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# Pour SMTP en production :
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=votre@email.com
# EMAIL_HOST_PASSWORD=votre-mot-de-passe-application

# ── Cache Redis (production) ──────────────────────────────────
# Laisser vide pour utiliser LocMemCache (développement)
# REDIS_URL=redis://localhost:6379/0

# ── Fichiers médias ──────────────────────────────────────────
MEDIA_ROOT=media/
MEDIA_URL=/media/
```

### Variables d'environnement requises en production

| Variable                | Description                             | Exemple                         |
| ----------------------- | --------------------------------------- | ------------------------------- |
| `SECRET_KEY`          | Clé secrète Django (50+ caractères)  | `django-insecure-...`         |
| `DEBUG`               | Mode debug (toujours `False` en prod) | `False`                       |
| `ALLOWED_HOSTS`       | Domaines autorisés                     | `monsite.com,www.monsite.com` |
| `DATABASE_URL`        | URL de la base de données              | `postgres://...`              |
| `REDIS_URL`           | URL Redis pour le cache                 | `redis://localhost:6379/0`    |
| `EMAIL_HOST_USER`     | Email expéditeur                       | `noreply@transport.com`       |
| `EMAIL_HOST_PASSWORD` | Mot de passe email                      | `app-password`                |

---

## 🚀 Lancer le projet

### Développement

```bash
# Activer l'environnement virtuel
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Lancer le serveur
python manage.py runserver

# Accès :
# Application :  http://127.0.0.1:8000/
# Admin Django : http://127.0.0.1:8000/admin/
# API Browser :  http://127.0.0.1:8000/api/
```

### Commandes utiles

```bash
# Créer les migrations après modification des modèles
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques (production)
python manage.py collectstatic --noinput

# Vérifier la configuration Django
python manage.py check

# Ouvrir le shell interactif
python manage.py shell

# Lancer les tests
python manage.py test apps.reservations --verbosity=2
```

---

## 🔌 Aperçu des endpoints API

L'API REST est accessible sous le préfixe `/api/`. Authentification par **Token** ou **Session**.

### Obtenir un token d'authentification

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "motdepasse"}'
```

### Endpoints principaux

| Méthode | Endpoint                            | Description                             | Auth requise |
| -------- | ----------------------------------- | --------------------------------------- | :----------: |
| `GET`  | `/api/trajets/`                   | Liste tous les trajets                  |      ✅      |
| `GET`  | `/api/trajets/disponibles/`       | Trajets avec places dispo (caché 5min) |      ✅      |
| `GET`  | `/api/trajets/{id}/`              | Détail d'un trajet                     |      ✅      |
| `GET`  | `/api/reservations/`              | Mes réservations                       |      ✅      |
| `POST` | `/api/reservations/`              | Créer une réservation                 |      ✅      |
| `GET`  | `/api/reservations/{id}/`         | Détail d'une réservation              |      ✅      |
| `POST` | `/api/reservations/{id}/annuler/` | Annuler une réservation                |      ✅      |
| `GET`  | `/api/reservations/{id}/billet/`  | Télécharger le billet PDF             |      ✅      |
| `GET`  | `/api/bus/`                       | Liste des bus (admin)                   |      🔐      |
| `POST` | `/api/bus/`                       | Créer un bus (admin)                   |      🔐      |
| `GET`  | `/api/accounts/me/`               | Profil de l'utilisateur connecté       |      ✅      |

> 📖 [Documentation complète de l&#39;API →](07_DOCUMENTATION_API.md)

---

## 🧪 Tests

### Lancer la suite de tests complète

```bash
# Tests du module réservations (31 tests)
python manage.py test apps.reservations --verbosity=2

# Tests de tous les modules
python manage.py test apps --verbosity=2

# Avec mesure de couverture
coverage run manage.py test apps.reservations
coverage report -m
coverage html  # Rapport HTML dans htmlcov/
```

### Résultats actuels

```
System check identified no issues (0 silenced).
...........................................................................
----------------------------------------------------------------------
Ran 31 tests in 23.391s

OK
```

### Couverture par module

| Module                |    Tests    |         Statut         |
| --------------------- | :----------: | :---------------------: |
| `apps.reservations` |      31      |          ✅ OK          |
| `apps.trajets`      |      9      | ⚠️ 1 erreur (BUG-003) |
| `apps.accounts`     |      —      |           —           |
| `apps.bus`          |      —      |           —           |
| **Total**       | **40** |     **39/40**     |

> 📋 [Rapport de tests détaillé →](02_PLAN_DE_TESTS.md)

---

## 📁 Structure du projet

```
transport-reservation/
│
├── 📄 manage.py                      # Point d'entrée Django
├── 📄 requirements.txt               # Dépendances Python
├── 📄 .env.example                   # Template variables d'env
├── 📄 .gitignore                     # Fichiers ignorés par Git
│
├── 📁 transport_project/             # Configuration principale
│   ├── settings.py                   # Paramètres Django
│   ├── urls.py                       # URLs racine
│   ├── wsgi.py                       # Interface WSGI (Gunicorn)
│   └── asgi.py                       # Interface ASGI (Daphne)
│
├── 📁 apps/                          # Applications Django
│   ├── 📁 accounts/                  # Gestion des utilisateurs
│   │   ├── models.py                 # Modèle User personnalisé
│   │   ├── views.py                  # Inscription, connexion, profil
│   │   ├── forms.py                  # Formulaires auth
│   │   ├── serializers.py            # Sérialiseurs API
│   │   ├── urls.py                   # URLs HTML
│   │   └── api_urls.py               # URLs API REST
│   │
│   ├── 📁 bus/                       # Gestion de la flotte
│   │   ├── models.py                 # Modèle Bus
│   │   ├── views.py                  # CRUD bus (admin)
│   │   ├── admin.py                  # Admin avec badge_statut
│   │   ├── serializers.py            # Sérialiseurs API
│   │   ├── urls.py                   # URLs HTML
│   │   └── api_urls.py               # URLs API REST
│   │
│   ├── 📁 trajets/                   # Gestion des trajets
│   │   ├── models.py                 # Modèle Trajet
│   │   ├── views.py                  # Liste + filtres avancés + cache
│   │   ├── forms.py                  # Formulaires trajets + filtres
│   │   ├── serializers.py            # Sérialiseurs API
│   │   ├── urls.py                   # URLs HTML
│   │   └── api_urls.py               # URLs API REST
│   │
│   └── 📁 reservations/              # Cœur métier
│       ├── models.py                 # Reservation + remboursement
│       ├── views.py                  # Dashboard, création, PDF, stats, CSV
│       ├── forms.py                  # Formulaires réservation
│       ├── serializers.py            # Sérialiseurs API
│       ├── pdf_generator.py          # BilletPDFGenerator (ReportLab)
│       ├── email_service.py          # EmailBilletService
│       ├── tests.py                  # 31 tests (8 classes)
│       ├── urls.py                   # URLs HTML (9 patterns)
│       └── api_urls.py               # URLs API REST
│
├── 📁 templates/                     # Templates HTML (22 fichiers)
│   ├── base.html                     # Template de base
│   ├── home.html                     # Page d'accueil
│   ├── accounts/                     # Templates auth
│   ├── bus/                          # Templates bus
│   ├── trajets/                      # Templates trajets
│   └── reservations/                 # Templates réservations
│
├── 📁 static/                        # Fichiers statiques
│   └── css/                          # Feuilles de style
│
├── 📁 media/                         # Fichiers médias (billets PDF)
├── 📁 logs/                          # Fichiers de logs rotatifs
│   ├── transport.log                 # Log général
│   ├── errors.log                    # Erreurs uniquement
│   └── reservations.log             # Logs réservations
│
└── 📁 fixtures/                      # Données de démonstration
    └── demo_data.json
```

---

## 👥 Équipe & Sprints

### Organisation Agile

| Sprint   | Période        | Fonctionnalités                            | Statut |
| -------- | --------------- | ------------------------------------------- | :----: |
| Sprint 1 | 18–19 Nov 2024 | F01, F02, F03 (PDF, Email, Dashboard)       |   ✅   |
| Sprint 2 | 19–20 Nov 2024 | F04, F05 (Stats, CSV Export)                |   ✅   |
| Sprint 3 | 20–21 Nov 2024 | F06, F07, F08 (Annulation, Filtres, Notifs) |   ✅   |
| Sprint 4 | 21 Nov 2024     | F09, F10, F11, F12 (API, Logs, Cache, RBAC) |   ✅   |

### Tags Git

| Tag        | Commit  | Description                     |
| ---------- | ------- | ------------------------------- |
| `v1.0.0` | 53cab66 | Base projet (Sprint 1 complet)  |
| `v2.0.0` | 2ed680e | Version complète (12 features) |

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](../transport_project/LICENSE) pour les détails.

```
MIT License — Transport Réservation v2.0
Copyright (c) 2024 — Équipe DevOps
```

---

## 📎 Liens de navigation

| Document                                                     | Description                                |
| ------------------------------------------------------------ | ------------------------------------------ |
| [📊 Rapport Analyse Technique](01_RAPPORT_ANALYSE_TECHNIQUE.md) | Architecture, modèles, vues, API          |
| [📋 Plan de Tests](02_PLAN_DE_TESTS.md)                         | 53 cas de tests + matrice de traçabilité |
| [🐛 Rapport d&#39;Anomalies](03_RAPPORT_ANOMALIES.md)           | 6 bugs (2 résolus, 4 ouverts)             |
| [📖 Guide Utilisateur](05_GUIDE_UTILISATEUR.md)                 | Parcours utilisateur pas à pas            |
| [🔧 Guide Administrateur](06_GUIDE_ADMINISTRATEUR.md)           | Panel admin, gestion du parc               |
| [🔌 Documentation API](07_DOCUMENTATION_API.md)                 | Référence complète API REST             |
| [📝 Changelog](08_CHANGELOG.md)                                 | Historique des versions par sprint         |
| [🤝 Guide Contribution](09_GUIDE_CONTRIBUTION.md)               | Conventions, PR, issues                    |
| [🚀 Plan Déploiement](10_PLAN_DEPLOIEMENT.md)                  | Checklist production                       |

---

<div align="center">


</div>
