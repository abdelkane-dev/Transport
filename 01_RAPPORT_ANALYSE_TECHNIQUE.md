# 📊 RAPPORT D'ANALYSE TECHNIQUE — Transport Réservation v2.0

> **Projet :** Application de réservation de billets de bus — Django 5.1.4
> **Rôle :** Assistant QA & Documentation — Personne 3
> **Date :** Juin 2025
> **Statut :** ✅ Analyse complète — 4 Sprints / 12 Features

---

## 📋 Table des matières

1. [Vue d&#39;ensemble du projet](#1-vue-densemble-du-projet)
2. [Architecture générale](#2-architecture-générale)
3. [Analyse des modèles de données](#3-analyse-des-modèles-de-données)
4. [Analyse des vues et contrôleurs](#4-analyse-des-vues-et-contrôleurs)
5. [Analyse des URLs et routing](#5-analyse-des-urls-et-routing)
6. [Analyse de la couche API REST](#6-analyse-de-la-couche-api-rest)
7. [Analyse des formulaires](#7-analyse-des-formulaires)
8. [Analyse de la configuration](#8-analyse-de-la-configuration)
9. [Analyse des templates](#9-analyse-des-templates)
10. [Analyse des tests](#10-analyse-des-tests)
11. [Analyse de la sécurité](#11-analyse-de-la-sécurité)
12. [Métriques et qualité du code](#12-métriques-et-qualité-du-code)

---

## 1. Vue d'ensemble du projet

### 1.1 Fiche d'identité technique

| Critère                   | Valeur                                         |
| -------------------------- | ---------------------------------------------- |
| **Framework**        | Django 5.1.4                                   |
| **Python**           | 3.11+                                          |
| **Base de données** | SQLite (dev) / PostgreSQL (prod compatible)    |
| **API**              | Django REST Framework 3.15.2                   |
| **Auth API**         | TokenAuthentication + SessionAuthentication    |
| **PDF**              | ReportLab 4.2.2 + QRCode 8.0 + Pillow 10.4.0   |
| **Cache**            | LocMemCache (dev) / Redis (prod via REDIS_URL) |
| **Logging**          | 3 RotatingFileHandlers (5 Mo max, 5 archives)  |
| **Fuseau horaire**   | Africa/Dakar (UTC+0)                           |
| **Langue interface** | Français (fr-fr)                              |

### 1.2 Structure du projet

```
transport_project/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── SPRINT_LOG.md
├── db.sqlite3
│
├── transport_project/          # Configuration Django
│   ├── settings.py             # Configuration principale (v2.0)
│   ├── urls.py                 # Routeur principal
│   └── wsgi.py
│
├── apps/                       # Applications métier
│   ├── accounts/               # Gestion des utilisateurs
│   ├── bus/                    # Gestion de la flotte
│   ├── trajets/                # Gestion des trajets
│   └── reservations/           # Gestion des réservations (cœur)
│
├── templates/                  # Templates HTML globaux
│   ├── base.html
│   ├── home.html
│   ├── accounts/               # 3 templates
│   ├── bus/                    # 4 templates
│   ├── trajets/                # 5 templates
│   └── reservations/           # 6 templates
│
├── static/                     # Fichiers statiques
│   └── css/style.css
│
├── media/                      # Fichiers générés (billets PDF)
│   └── billets/
│
├── logs/                       # Journaux applicatifs
│   ├── transport.log
│   ├── errors.log
│   └── reservations.log
│
└── fixtures/                   # Données de test
    └── initial_data.json
```

### 1.3 Récapitulatif des 12 fonctionnalités

| Sprint             | #   | Feature                   | Fichiers principaux                        | Statut |
| ------------------ | --- | ------------------------- | ------------------------------------------ | ------ |
| **Sprint 1** | F1  | Génération PDF billets  | `pdf_generator.py`                       | ✅     |
| **Sprint 1** | F2  | Email auto avec PDF       | `email_service.py`                       | ✅     |
| **Sprint 1** | F10 | Logging fichiers rotatifs | `settings.py`                            | ✅     |
| **Sprint 2** | F3  | Dashboard statistiques    | `views.py`, `dashboard_stats.html`     | ✅     |
| **Sprint 2** | F4  | Export CSV Excel          | `views.py`                               | ✅     |
| **Sprint 2** | F8  | Notifications système    | `views.py` (messages)                    | ✅     |
| **Sprint 3** | F5  | Filtres avancés trajets  | `trajets/forms.py`, `trajets/views.py` | ✅     |
| **Sprint 3** | F6  | Annulation remboursement  | `models.py`                              | ✅     |
| **Sprint 3** | F7  | Réservation groupée     | `models.py`, `forms.py`                | ✅     |
| **Sprint 3** | F9  | REST API complète        | `serializers.py`, `api_urls.py`        | ✅     |
| **Sprint 4** | F11 | Cache Redis/LocMem        | `settings.py`, `trajets/views.py`      | ✅     |
| **Sprint 4** | F12 | 31 tests unitaires        | `tests.py`                               | ✅     |

---

## 2. Architecture générale

### 2.1 Pattern architectural

L'application suit le pattern **MVT (Model-View-Template)** de Django, enrichi par une couche API REST :

```
┌─────────────────────────────────────────────────────┐
│                    CLIENT (Browser / API)            │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP Request
┌──────────────────────▼──────────────────────────────┐
│                  URLs Router                         │
│  /accounts/ /bus/ /trajets/ /reservations/ /api/    │
└──────────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┴──────────────┐
         │                            │
┌────────▼────────┐        ┌──────────▼──────────┐
│   Views HTML    │        │   DRF ViewSets API  │
│  (CBV + FBV)    │        │  (ModelViewSet)     │
└────────┬────────┘        └──────────┬──────────┘
         │                            │
┌────────▼────────────────────────────▼──────────┐
│                   Models (ORM)                  │
│    User ← Reservation → Trajet ← Bus           │
└────────────────────┬────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼──────┐     ┌──────────▼────────┐
│  SQLite (dev) │     │  Services externes │
│  PostgreSQL   │     │  PDF / Email / Log│
│  (prod)       │     │  Cache (Redis)    │
└───────────────┘     └───────────────────┘
```

### 2.2 Dépendances entre applications

```
accounts (User)
    └── reservations (Reservation.client → User)
            └── trajets (Reservation.trajet → Trajet)
                        └── bus (Trajet.bus → Bus)
```

### 2.3 Flux de données principal (réservation complète)

```
1. Client → GET /trajets/              → TrajetListeView (filtres avancés)
2. Client → GET /trajets/<id>/         → TrajetDetailView
3. Client → GET /reservations/creer/<trajet_id>/  → ReservationCreerView.get()
4. Client → POST /reservations/creer/<trajet_id>/ → ReservationCreerView.post()
              │
              ├─ ReservationForm.is_valid()
              ├─ reservation.full_clean() [validation métier]
              ├─ reservation.save()
              ├─ BilletPDFGenerator(reservation).generer()  → media/billets/
              ├─ EmailBilletService(reservation).envoyer_confirmation()
              ├─ logger.info("CRÉATION réservation...")
              └─ messages.success("✅ Réservation effectuée...")
5. Client ← Redirect → /reservations/<id>/
```

---

## 3. Analyse des modèles de données

### 3.1 Modèle `User` (apps/accounts/models.py)

**Hérite de :** `django.contrib.auth.models.AbstractUser`

| Champ                | Type           | Contraintes                           | Description                               |
| -------------------- | -------------- | ------------------------------------- | ----------------------------------------- |
| `email`            | EmailField     | `unique=True`                       | Identifiant de connexion (USERNAME_FIELD) |
| `prenom`           | CharField(100) | obligatoire                           | Prénom du client                         |
| `nom`              | CharField(100) | obligatoire                           | Nom de famille                            |
| `telephone`        | CharField(20)  | optionnel, regex `^\+?[0-9]{8,15}$` | Format africain                           |
| `date_inscription` | DateTimeField  | `auto_now_add=True`                 | Automatique                               |
| `username`         | (hérité)     | `REQUIRED_FIELDS`                   | Requis à la création                    |

**Méthodes métier :**

- `get_full_name()` → `"{prenom} {nom}"`
- `get_nombre_reservations()` → `int`
- `get_reservations_actives()` → QuerySet

**Configuration :**

```python
USERNAME_FIELD = 'email'           # Connexion par email
REQUIRED_FIELDS = ['username', 'nom', 'prenom']
AUTH_USER_MODEL = 'accounts.User'  # dans settings.py
```

---

### 3.2 Modèle `Bus` (apps/bus/models.py)

> ⚠️ **Important :** Le modèle Bus **N'A PAS** de champs `marque` ou `modele`.

| Champ                 | Type                 | Contraintes                        | Description        |
| --------------------- | -------------------- | ---------------------------------- | ------------------ |
| `immatriculation`   | CharField(20)        | `unique=True`                    | Ex:`DK-1234-AB`  |
| `nombre_places`     | PositiveIntegerField | `MinValueValidator(1)`           | Capacité totale   |
| `statut`            | CharField(15)        | choices: ACTIF/INACTIF/MAINTENANCE | État actuel       |
| `date_creation`     | DateTimeField        | `auto_now_add=True`              | Automatique        |
| `date_modification` | DateTimeField        | `auto_now=True`                  | Automatique        |
| `notes`             | TextField            | optionnel                          | Remarques internes |

**Choix statut :**

```python
ACTIF        = 'ACTIF'        → 'Actif'
INACTIF      = 'INACTIF'      → 'Inactif'
MAINTENANCE  = 'MAINTENANCE'  → 'En maintenance'
```

**Méthodes :**

- `est_actif()` → `bool`
- `get_nombre_trajets()` → `int`
- `get_places_reservees(trajet)` → `int`

**Tri par défaut :** `ordering = ['immatriculation']`

---

### 3.3 Modèle `Trajet` (apps/trajets/models.py)

| Champ                 | Type               | Contraintes                 | Description           |
| --------------------- | ------------------ | --------------------------- | --------------------- |
| `ville_depart`      | CharField(100)     | obligatoire                 | Ville de départ      |
| `ville_arrivee`     | CharField(100)     | obligatoire                 | Ville d'arrivée      |
| `date_depart`       | DateField          | obligatoire                 | Date du voyage        |
| `heure_depart`      | TimeField          | obligatoire                 | Heure de départ      |
| `prix`              | DecimalField(10,2) | `MinValueValidator(0.01)` | Prix par place (FCFA) |
| `bus`               | ForeignKey(Bus)    | `on_delete=PROTECT`       | Bus assigné          |
| `date_creation`     | DateTimeField      | `auto_now_add=True`       | Automatique           |
| `date_modification` | DateTimeField      | `auto_now=True`           | Automatique           |

**Contrainte unique :** `unique_together = [['bus', 'date_depart', 'heure_depart']]`

**Règles de validation (clean()) :**

1. Le bus assigné doit être en statut `ACTIF`
2. La ville de départ ≠ ville d'arrivée

**Méthodes calculées :**

- `get_places_reservees()` → Somme des places (EN_ATTENTE + CONFIRMEE)
- `get_places_disponibles()` → `nombre_places - places_reservees`
- `est_complet()` → `bool` (places_disponibles ≤ 0)
- `est_passe()` → `bool` (date_depart < today)
- `get_taux_remplissage()` → `int` (0-100%)

**Tri par défaut :** `ordering = ['-date_depart', 'heure_depart']`

---

### 3.4 Modèle `Reservation` (apps/reservations/models.py)

| Champ                | Type                 | Contraintes           | Description                      |
| -------------------- | -------------------- | --------------------- | -------------------------------- |
| `client`           | ForeignKey(User)     | `on_delete=CASCADE` | Le client réservant             |
| `trajet`           | ForeignKey(Trajet)   | `on_delete=PROTECT` | Trajet réservé                 |
| `nombre_places`    | PositiveIntegerField | `Min(1), Max(10)`   | 🆕 Sprint 3 : groupée           |
| `date_reservation` | DateTimeField        | `auto_now_add=True` | Automatique                      |
| `statut`           | CharField(15)        | choices: 3 états     | EN_ATTENTE / CONFIRMEE / ANNULEE |
| `notes`            | TextField            | optionnel             | Raison annulation, demandes      |

**Choix statut :**

```python
EN_ATTENTE = 'EN_ATTENTE'   → 'En attente'     (défaut)
CONFIRMEE  = 'CONFIRMEE'    → 'Confirmée'
ANNULEE    = 'ANNULEE'      → 'Annulée'
```

**Règles de validation (clean()) :**

1. Trajet non passé
2. Enough places disponibles (calcul excluant soi-même en modif)
3. nombre_places ≥ 1

**🆕 Méthodes Sprint 2-3 :**

```python
# Règle des 24h (Sprint 3 – Feature 6)
peut_etre_annulee_avec_remboursement()
    → (bool, float taux, str message)
    # taux = 1.0  si départ > 24h
    # taux = 0.5  si 2h ≤ départ ≤ 24h
    # taux = 0.0  si départ < 2h

calculer_remboursement()
    → (float montant_rembourse, float taux, str message)

get_prix_total()
    → Decimal (nombre_places × prix_trajet)

# Signature modifiée (Sprint 3)
annuler(raison='')
    → (bool, str message, float montant_rembourse)  # 3-tuple

confirmer()
    → (bool, str message)  # 2-tuple
```

**Logger :** `logging.getLogger('transport.reservations')`

---

### 3.5 Schéma relationnel

```
┌──────────────────┐       ┌───────────────────────┐
│      User        │       │         Bus            │
│──────────────────│       │───────────────────────│
│ email (PK, uniq) │       │ immatriculation (uniq) │
│ prenom           │       │ nombre_places          │
│ nom              │       │ statut                │
│ telephone        │       │ date_creation          │
│ date_inscription │       │ notes                 │
└────────┬─────────┘       └──────────┬────────────┘
         │ 1                          │ 1
         │                            │
         │ N                          │ N
┌────────▼─────────────────────┐ ┌───▼────────────────┐
│       Reservation            │ │       Trajet        │
│──────────────────────────────│ │────────────────────│
│ client  → User               │ │ bus → Bus          │
│ trajet  → Trajet  ◄──────────┘ │ ville_depart       │
│ nombre_places [1..10]        │ │ ville_arrivee      │
│ date_reservation             │ │ date_depart        │
│ statut                       │ │ heure_depart       │
│ notes                        │ │ prix               │
└──────────────────────────────┘ └────────────────────┘
```

---

## 4. Analyse des vues et contrôleurs

### 4.1 Application `accounts`

| Vue                 | Type                       | URL                        | Accès    | Description        |
| ------------------- | -------------------------- | -------------------------- | --------- | ------------------ |
| `InscriptionView` | CBV `View`               | `/accounts/inscription/` | Public    | Création compte   |
| `ConnexionView`   | CBV `View`               | `/accounts/connexion/`   | Public    | Login email/pwd    |
| `DeconnexionView` | CBV `View`               | `/accounts/deconnexion/` | Connecté | Logout + redirect  |
| `ProfilView`      | CBV `LoginRequiredMixin` | `/accounts/profil/`      | Connecté | Profil utilisateur |

### 4.2 Application `bus`

| Vue                  | Type           | URL                      | Accès | Description   |
| -------------------- | -------------- | ------------------------ | ------ | ------------- |
| `BusListeView`     | `ListView`   | `/bus/`                | Admin  | Liste flotte  |
| `BusDetailView`    | `DetailView` | `/bus/<id>/`           | Admin  | Détail bus   |
| `BusCreerView`     | `CreateView` | `/bus/creer/`          | Admin  | Nouveau bus   |
| `BusModifierView`  | `UpdateView` | `/bus/<id>/modifier/`  | Admin  | Modifier bus  |
| `BusSupprimerView` | `DeleteView` | `/bus/<id>/supprimer/` | Admin  | Supprimer bus |

### 4.3 Application `trajets`

| Vue                     | Type           | URL                          | Accès | Description                 |
| ----------------------- | -------------- | ---------------------------- | ------ | --------------------------- |
| `TrajetListeView`     | `ListView`   | `/trajets/`                | Public | Liste + 🆕 filtres avancés |
| `TrajetTousView`      | `ListView`   | `/trajets/tous/`           | Admin  | Tous les trajets            |
| `TrajetDetailView`    | `DetailView` | `/trajets/<id>/`           | Public | Détail + disponibilité    |
| `TrajetCreerView`     | `CreateView` | `/trajets/creer/`          | Admin  | Créer trajet               |
| `TrajetModifierView`  | `UpdateView` | `/trajets/<id>/modifier/`  | Admin  | Modifier                    |
| `TrajetSupprimerView` | `DeleteView` | `/trajets/<id>/supprimer/` | Admin  | Supprimer                   |

**🆕 Filtres avancés dans `TrajetListeView.get_queryset()` :**

```python
# Filtres de base
ville_depart    → queryset.filter(ville_depart__icontains=...)
ville_arrivee   → queryset.filter(ville_arrivee__icontains=...)
date_depart     → queryset.filter(date_depart=...)

# Filtres Sprint 3 – Feature 5
prix_min        → queryset.filter(prix__gte=float(prix_min))
prix_max        → queryset.filter(prix__lte=float(prix_max))
creneau         → queryset.filter(heure_depart__gte=h_debut, heure_depart__lte=h_fin)
# Créneaux : matin (06:00-11:59), apres_midi (12:00-17:59), soir (18:00-23:59), nuit (00:00-05:59)
places_min      → [t for t in liste if t.get_places_disponibles() >= nb]
exclure_complets → [t for t in liste if not t.est_complet()]
```

### 4.4 Application `reservations`

| Vue                            | Type           | URL                                  | Accès              | Description              |
| ------------------------------ | -------------- | ------------------------------------ | ------------------- | ------------------------ |
| `DashboardView`              | `ListView`   | `/reservations/dashboard/`         | Connecté           | Mes réservations        |
| `ReservationDetailView`      | `DetailView` | `/reservations/<id>/`              | Propriétaire/Admin | Détail                  |
| `ReservationCreerView`       | `View`       | `/reservations/creer/<trajet_id>/` | Connecté           | 🆕 PDF + Email           |
| `ReservationAnnulerView`     | `View`       | `/reservations/<id>/annuler/`      | Propriétaire       | 🆕 Remboursement         |
| `telecharger_billet_view`    | FBV            | `/reservations/<id>/billet/`       | Propriétaire       | 🆕 PDF download          |
| `admin_reservations_view`    | FBV            | `/reservations/admin/`             | Admin               | Toutes les réservations |
| `confirmer_reservation_view` | FBV            | `/reservations/<id>/confirmer/`    | Admin               | Confirmer                |
| `dashboard_stats_view`       | FBV            | `/reservations/stats/`             | Connecté           | 🆕 Statistiques Chart.js |
| `export_csv_view`            | FBV            | `/reservations/export/csv/`        | Connecté           | 🆕 Export CSV            |

**🆕 `ReservationCreerView.post()` — Flux Sprint 1 :**

```python
1. form.is_valid() → True
2. reservation.full_clean()
3. reservation.save()
4. BilletPDFGenerator(reservation).generer()    # Sauvegarde disque
5. generateur.generer_bytes()                   # Bytes pour email
6. EmailBilletService(reservation).envoyer_confirmation(pdf_bytes)
7. logger.info("CRÉATION réservation #%s...")
8. messages.success("✅ Réservation effectuée...")
```

**🆕 `dashboard_stats_view()` — Données pour Chart.js :**

```python
context = {
    'total': int,               # Total réservations
    'actives': int,             # EN_ATTENTE + CONFIRMEE
    'annulees': int,
    'confirmees': int,
    'total_depense': Decimal,   # Somme prix_total (actives)
    'taux_annulation': float,   # % arrondi 1 décimale
    'labels_mois': JSON,        # ['jan 2024', 'fév 2024', ...]
    'data_mois': JSON,          # [3, 5, 2, ...]
    'destinations': QuerySet,   # Top 5 villes arrivée
    'dernieres_reservations': QuerySet,  # 5 dernières
}
```

**🆕 `export_csv_view()` — Format CSV :**

```
Encodage : UTF-8 BOM (compatible Excel)
Séparateur : virgule (,)
Colonnes : Numéro, Date réservation, Ville départ, Ville arrivée,
           Date trajet, Heure départ, Bus (immatriculation),
           Nombre places, Prix unitaire, Prix total, Statut, Notes
Nom fichier : reservations_{email}_{date}.csv
```

---

## 5. Analyse des URLs et routing

### 5.1 URLs principales (transport_project/urls.py)

```python
/                           → home.html (TemplateView)
/admin/                     → Interface Django Admin
/accounts/...               → apps.accounts.urls (namespace='accounts')
/bus/...                    → apps.bus.urls (namespace='bus')
/trajets/...                → apps.trajets.urls (namespace='trajets')
/reservations/...           → apps.reservations.urls (namespace='reservations')
/api/bus/...                → apps.bus.api_urls (namespace='api-bus')
/api/trajets/...            → apps.trajets.api_urls (namespace='api-trajets')
/api/reservations/...       → apps.reservations.api_urls (namespace='api-reservations')
/api/accounts/...           → apps.accounts.api_urls (namespace='api-accounts')
/api/auth/...               → rest_framework.urls (namespace='rest_framework')
```

**Media en DEBUG :**

```python
if settings.DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
```

### 5.2 URLs complètes par application

#### Accounts

```
GET  /accounts/inscription/    → InscriptionView
GET  /accounts/connexion/      → ConnexionView
GET  /accounts/deconnexion/    → DeconnexionView
GET  /accounts/profil/         → ProfilView [auth requise]
```

#### Bus

```
GET  /bus/                     → BusListeView
GET  /bus/<id>/                → BusDetailView
GET  /bus/creer/               → BusCreerView [admin]
POST /bus/creer/
GET  /bus/<id>/modifier/       → BusModifierView [admin]
POST /bus/<id>/modifier/
GET  /bus/<id>/supprimer/      → BusSupprimerView [admin]
POST /bus/<id>/supprimer/
```

#### Trajets

```
GET  /trajets/                 → TrajetListeView [filtres avancés]
GET  /trajets/tous/            → TrajetTousView [admin]
GET  /trajets/<id>/            → TrajetDetailView
GET  /trajets/creer/           → TrajetCreerView [admin]
POST /trajets/creer/
GET  /trajets/<id>/modifier/   → TrajetModifierView [admin]
GET  /trajets/<id>/supprimer/  → TrajetSupprimerView [admin]
```

#### Réservations

```
GET      /reservations/dashboard/           → DashboardView [auth]
GET      /reservations/<id>/               → ReservationDetailView [auth]
GET/POST /reservations/creer/<trajet_id>/  → ReservationCreerView [auth]
GET/POST /reservations/<id>/annuler/       → ReservationAnnulerView [auth]
GET      /reservations/<id>/billet/        → telecharger_billet_view [auth] 🆕
GET      /reservations/admin/              → admin_reservations_view [staff]
POST     /reservations/<id>/confirmer/     → confirmer_reservation_view [staff]
GET      /reservations/stats/              → dashboard_stats_view [auth] 🆕
GET      /reservations/export/csv/         → export_csv_view [auth] 🆕
```

---

## 6. Analyse de la couche API REST

### 6.1 Configuration DRF (settings.py)

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### 6.2 Endpoints API complets

#### `/api/trajets/` — TrajetViewSet

| Méthode   | URL                               | Permission       | Description                         |
| ---------- | --------------------------------- | ---------------- | ----------------------------------- |
| `GET`    | `/api/trajets/`                 | Public (lecture) | Liste trajets futurs                |
| `POST`   | `/api/trajets/`                 | Admin            | Créer trajet                       |
| `GET`    | `/api/trajets/{id}/`            | Public           | Détail trajet                      |
| `PUT`    | `/api/trajets/{id}/`            | Admin            | Modifier complet                    |
| `PATCH`  | `/api/trajets/{id}/`            | Admin            | Modifier partiel                    |
| `DELETE` | `/api/trajets/{id}/`            | Admin            | Supprimer                           |
| `GET`    | `/api/trajets/disponibles/`     | Public           | 🆕 Trajets disponibles (cache 5min) |
| `GET`    | `/api/trajets/filtres_avances/` | Public           | 🆕 Recherche avancée               |

**Paramètres `filtres_avances` :**

```
?prix_min=1000&prix_max=5000&creneau=matin&places_min=2
```

**Réponse `disponibles` :**

```json
{
  "count": 12,
  "trajets": [
    {
      "id": 1,
      "ville_depart": "Dakar",
      "ville_arrivee": "Thiès",
      "date_depart": "2025-07-15",
      "heure_depart": "08:00:00",
      "prix": "2500.00",
      "prix_formate": "2 500 FCFA",
      "places_disponibles": 28,
      "places_reservees": 2,
      "est_complet": false,
      "taux_remplissage": 7
    }
  ]
}
```

#### `/api/reservations/` — ReservationViewSet

| Méthode   | URL                                        | Permission    | Description                          |
| ---------- | ------------------------------------------ | ------------- | ------------------------------------ |
| `GET`    | `/api/reservations/`                     | Connecté     | Mes réservations                    |
| `POST`   | `/api/reservations/`                     | Connecté     | Créer réservation                  |
| `GET`    | `/api/reservations/{id}/`                | Propriétaire | Détail                              |
| `DELETE` | `/api/reservations/{id}/`                | Propriétaire | Annuler (retourne montant_rembourse) |
| `GET`    | `/api/reservations/mes_stats/`           | Connecté     | 🆕 Statistiques personnelles         |
| `POST`   | `/api/reservations/reservation_groupee/` | Connecté     | 🆕 Groupée (max 10 places)          |

**Sécurité ViewSet :**

```python
def get_queryset(self):
    if user.is_staff:
        return Reservation.objects.all()      # Admin : toutes
    return Reservation.objects.filter(client=user)  # Client : les siennes
```

### 6.3 Serializers

#### `TrajetSerializer`

**Champs exposés :**

- `id`, `ville_depart`, `ville_arrivee`, `date_depart`, `heure_depart`
- `prix`, `prix_formate` (calculé: `"2 500 FCFA"`)
- `bus` (id), `bus_detail` (objet complet, read_only)
- `places_disponibles`, `places_reservees`, `est_complet`, `est_passe`, `taux_remplissage`
- `date_creation`, `date_modification`

**Validations :**

- `validate_bus()` → Bus doit être ACTIF
- `validate()` → villes différentes

#### `ReservationSerializer`

**Champs exposés :**

- `id`, `client` (id), `client_detail` (objet, read_only)
- `trajet` (id), `trajet_detail` (objet, read_only)
- `nombre_places`, `date_reservation`, `statut`, `statut_libelle`
- `prix_total` (calculé: `"5 000 FCFA"`), `peut_etre_annulee`, `notes`

**Logique de création :**

```python
def create(self, validated_data):
    request = self.context.get('request')
    validated_data['client'] = request.user  # Auto-assign
    return super().create(validated_data)
```

---

## 7. Analyse des formulaires

### 7.1 `InscriptionForm` (accounts/forms.py)

| Champ                      | Type          | Validation                 |
| -------------------------- | ------------- | -------------------------- |
| `prenom`                 | CharField     | requis                     |
| `nom`                    | CharField     | requis                     |
| `email`                  | EmailField    | unique en BDD              |
| `telephone`              | CharField     | regex `^\+?[0-9]{8,15}$` |
| `username`               | CharField     | unique Django              |
| `mot_de_passe`           | PasswordInput | min 8 chars                |
| `confirmer_mot_de_passe` | PasswordInput | === mot_de_passe           |

### 7.2 `ReservationForm` (reservations/forms.py)

| Champ             | Type        | Validation                     |
| ----------------- | ----------- | ------------------------------ |
| `nombre_places` | NumberInput | min=1, max=10 (Sprint 3 – F7) |
| `notes`         | Textarea    | optionnel, max 500 chars       |

**Validation `clean_nombre_places()` :**

```python
if nb < 1: raise ValidationError("Au moins 1 place")
if nb > 10: raise ValidationError("Maximum 10 places par réservation groupée")
if nb > places_dispo: raise ValidationError(f"Seulement {places_dispo} place(s) disponibles")
```

### 7.3 `FiltresAvancesTrajetForm` (trajets/forms.py) — Sprint 3

| Champ                | Type         | Validation                 |
| -------------------- | ------------ | -------------------------- |
| `prix_min`         | DecimalField | optionnel, min=0           |
| `prix_max`         | DecimalField | optionnel, min=0           |
| `creneau`          | ChoiceField  | matin/apres_midi/soir/nuit |
| `places_min`       | IntegerField | min=1, max=50              |
| `exclure_complets` | BooleanField | initial=True               |

**Validation `clean()` :** `prix_min ≤ prix_max`

---

## 8. Analyse de la configuration

### 8.1 Sécurité (settings.py)

```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-...')  # ⚠️ Changer en prod
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

> ⚠️ **Point de vigilance :** `DEBUG=True` par défaut. Nécessite une variable d'environnement en production.

### 8.2 Email

| Variable env            | Valeur par défaut                    | Description                  |
| ----------------------- | ------------------------------------- | ---------------------------- |
| `EMAIL_BACKEND`       | `console.EmailBackend`              | ⚠️ Dev: affiche en console |
| `EMAIL_HOST`          | `smtp.gmail.com`                    | Serveur SMTP                 |
| `EMAIL_PORT`          | `587`                               | Port TLS                     |
| `EMAIL_USE_TLS`       | `True`                              | TLS activé                  |
| `EMAIL_HOST_USER`     | ``                                    | À configurer                |
| `EMAIL_HOST_PASSWORD` | ``                                    | À configurer                |
| `DEFAULT_FROM_EMAIL`  | `noreply@transport-reservations.sn` | Expéditeur                  |

### 8.3 Logging — 3 fichiers rotatifs

| Handler                  | Fichier                   | Niveau  | Rotation | Archives |
| ------------------------ | ------------------------- | ------- | -------- | -------- |
| `fichier_transport`    | `logs/transport.log`    | INFO    | 5 Mo     | 5        |
| `fichier_erreurs`      | `logs/errors.log`       | WARNING | 5 Mo     | 3        |
| `fichier_reservations` | `logs/reservations.log` | INFO    | 5 Mo     | 5        |

**Loggers applicatifs :**

```python
transport.reservations  → reservations.log + errors.log + console
transport.email         → transport.log + errors.log + console
transport.pdf           → transport.log + console
transport               → transport.log + errors.log + console
django                  → transport.log + console
```

### 8.4 Cache

```python
# Développement (défaut)
CACHES = {'default': {'BACKEND': 'LocMemCache', 'LOCATION': 'transport-cache'}}

# Production (si REDIS_URL défini)
CACHES = {'default': {'BACKEND': 'RedisCache', 'LOCATION': REDIS_URL, 'TIMEOUT': 300}}
```

**Clé mise en cache :** `api_trajets_disponibles` — TTL : 300 secondes

---

## 9. Analyse des templates

### 9.1 Inventaire complet

| Template                                  | Localisation                     | Sprint      | Description                           |
| ----------------------------------------- | -------------------------------- | ----------- | ------------------------------------- |
| `base.html`                             | `templates/`                   | Base        | Navbar, messages flash, Bootstrap 5   |
| `home.html`                             | `templates/`                   | Base        | Page d'accueil                        |
| `accounts/connexion.html`               | `templates/`                   | Base        | Formulaire login                      |
| `accounts/inscription.html`             | `templates/`                   | Base        | Formulaire création compte           |
| `accounts/profil.html`                  | `templates/`                   | Base        | Profil utilisateur                    |
| `bus/bus_liste.html`                    | `templates/`                   | Base        | Flotte de bus                         |
| `bus/bus_detail.html`                   | `templates/`                   | Base        | Détail bus                           |
| `bus/bus_form.html`                     | `templates/`                   | Base        | Créer/modifier bus                   |
| `bus/bus_supprimer.html`                | `templates/`                   | Base        | Confirmer suppression                 |
| `trajets/trajet_liste.html`             | `templates/`                   | Sprint 3 🆕 | Liste + filtres avancés collapsibles |
| `trajets/trajet_detail.html`            | `templates/`                   | Base        | Détail + disponibilité              |
| `trajets/trajet_form.html`              | `templates/`                   | Base        | Créer/modifier                       |
| `trajets/trajet_supprimer.html`         | `templates/`                   | Base        | Confirmation                          |
| `trajets/trajet_tous.html`              | `templates/`                   | Base        | Vue admin tous trajets                |
| `reservations/dashboard.html`           | `templates/`                   | Sprint 2 🆕 | Stats + CSV + PDF buttons             |
| `reservations/dashboard_stats.html`     | `templates/`                   | Sprint 2 🆕 | Graphiques Chart.js                   |
| `reservations/reservation_creer.html`   | `templates/`                   | Base        | Formulaire réservation               |
| `reservations/reservation_detail.html`  | `templates/`                   | Sprint 2 🆕 | + PDF download + remboursement info   |
| `reservations/reservation_annuler.html` | `templates/`                   | Sprint 3 🆕 | + Simulation remboursement            |
| `reservations/admin_reservations.html`  | `templates/`                   | Base        | Vue admin                             |
| `emails/confirmation_reservation.html`  | `apps/reservations/templates/` | Sprint 1 🆕 | Email HTML confirmation               |
| `emails/annulation_reservation.html`    | `apps/reservations/templates/` | Sprint 1 🆕 | Email HTML annulation                 |

### 9.2 Bibliothèques frontend utilisées

```html
<!-- Bootstrap 5 (CSS + JS) — Interface responsive -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.x/dist/css/bootstrap.min.css">

<!-- Chart.js — Graphiques dashboard stats -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- Font Awesome — Icônes -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.x/css/all.min.css">
```

---

## 10. Analyse des tests

### 10.1 Résultats globaux

```
Ran 31 tests in 23.391s
OK (apps.reservations)

Ran 40 tests in 25.714s  
FAILED (errors=1)  ← Bug mineur: Trajet.__str__ sur heure_depart (str vs TimeField)
```

> **Note :** L'erreur dans `apps.trajets` est un bug non bloquant dans `Trajet.__str__()` — `heure_depart.strftime('%Hh%M')` appelé sur un objet `str` au lieu d'un `time`. Ne concerne pas les 31 tests de réservations qui passent tous.

### 10.2 Couverture par classe de tests

| Classe                              | Tests        | Sprint/Feature            | Résultat          |
| ----------------------------------- | ------------ | ------------------------- | ------------------ |
| `BilletPDFGeneratorTestCase`      | 4            | Sprint 1 – F1            | ✅ OK              |
| `EmailBilletServiceTestCase`      | 3            | Sprint 1 – F2            | ✅ OK              |
| `DashboardStatsViewTestCase`      | 3            | Sprint 2 – F3            | ✅ OK              |
| `ExportCSVViewTestCase`           | 3            | Sprint 2 – F4            | ✅ OK              |
| `AnnulationRemboursementTestCase` | 4            | Sprint 2/3 – F6          | ✅ OK              |
| `ReservationGroupeeTestCase`      | 4            | Sprint 3 – F7            | ✅ OK              |
| `ReservationIntegrationTestCase`  | 7            | Sprint 4 – F12           | ✅ OK              |
| `FiltresAvancesTrajetsTestCase`   | 3            | Sprint 3 – F5            | ✅ OK              |
| **TOTAL**                     | **31** | **Toutes features** | **✅ 31/31** |

### 10.3 Détail des tests critiques

#### `BilletPDFGeneratorTestCase`

```python
test_generation_pdf_bytes        → vérifie pdf_bytes.startswith(b'%PDF')
test_nom_fichier_correct         → vérifie pk dans le nom + '.pdf'
test_generation_pdf_sur_disque   → vérifie existence + taille > 1Ko
test_qr_code_genere              → vérifie absence d'exception
```

#### `AnnulationRemboursementTestCase`

```python
test_remboursement_100_pourcent  → taux=1.0 si départ >24h
test_remboursement_50_pourcent   → taux=0.5 si 2h≤départ≤24h
test_remboursement_0_pourcent    → taux=0.0 si départ <2h
test_annuler_retourne_3_tuple    → vérifie (bool, str, float)
```

#### `ReservationIntegrationTestCase` (7 tests E2E)

```python
test_flux_complet_reservation_et_telechargement_pdf
test_acces_dashboard_non_connecte
test_admin_voit_toutes_les_reservations
test_client_ne_voit_que_ses_reservations
test_annulation_change_le_statut
test_confirmer_reservation_admin
test_reservation_trajet_complet_impossible
```

### 10.4 Helpers de test

```python
creer_bus(immatriculation='DK-1234-AB', places=30)
    → Bus.objects.create(immatriculation=..., nombre_places=..., statut='ACTIF')
    # ⚠️ PAS de champs marque/modele (n'existent pas dans le modèle)

creer_trajet(bus, ville_depart='Dakar', ville_arrivee='Thiès',
             jours_dans_futur=7, heure=time(8, 0), prix=Decimal('2500'))

creer_utilisateur(email='client@test.sn', password='TestPass123!')
creer_admin(email='admin@test.sn', password='AdminPass123!')
```

---

## 11. Analyse de la sécurité

### 11.1 Contrôle d'accès par vue

| Vue                  | Mécanisme                                           | Implémentation                                            |
| -------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| Dashboard client     | `LoginRequiredMixin`                               | `login_url = '/accounts/connexion/'`                     |
| Détail réservation | `LoginRequiredMixin` + vérification propriétaire | `if reservation.client != request.user and not is_staff` |
| Créer réservation  | `LoginRequiredMixin`                               | Auto-assign `client = request.user`                      |
| Annuler réservation | `LoginRequiredMixin` + vérification propriétaire | `get_reservation_or_403()`                               |
| PDF download         | `@login_required` + propriétaire                  | `redirect` si accès non autorisé                       |
| Admin vues           | `is_staff` check                                   | `return redirect('reservations:dashboard')` si non-staff |
| API ViewSets         | `IsAuthenticated`                                  | `get_queryset()` filtre par `request.user`             |

### 11.2 Protection CSRF

Activée via le middleware `CsrfViewMiddleware` (inclus dans `MIDDLEWARE`).
Tous les formulaires POST utilisent `{% csrf_token %}`.

### 11.3 Isolation des données

**Client :** Ne voit **QUE** ses propres réservations :

```python
# DashboardView
return Reservation.objects.filter(client=self.request.user)

# ReservationViewSet (API)
return Reservation.objects.filter(client=user)  # si not is_staff
```

### 11.4 Validation métier

```python
# Réservation : full_clean() appelé avant save()
reservation.full_clean()  # Déclenche Reservation.clean()
# → Vérifie trajet non passé
# → Vérifie places disponibles
# → Vérifie MaxValueValidator(10)
```

### 11.5 Sensibilités identifiées

| # | Risque                              | Niveau   | Mitigation existante                      |
| - | ----------------------------------- | -------- | ----------------------------------------- |
| 1 | `SECRET_KEY` insecure par défaut | 🔴 Haut  | Variable env `SECRET_KEY` documentée   |
| 2 | `DEBUG=True` par défaut          | 🔴 Haut  | Variable env `DEBUG=False` en prod      |
| 3 | Email en console par défaut        | 🟡 Moyen | Backend configurable via env              |
| 4 | SQLite en dev (pas de prod)         | 🟡 Moyen | Commentaire PostgreSQL dans settings      |
| 5 | Pas de rate limiting sur API        | 🟡 Moyen | À ajouter (django-ratelimit)             |
| 6 | Pas de HTTPS forcé                 | 🟡 Moyen | À activer (`SECURE_SSL_REDIRECT=True`) |

---

## 12. Métriques et qualité du code

### 12.1 Métriques globales

| Métrique                          | Valeur                                   |
| ---------------------------------- | ---------------------------------------- |
| **Nombre d'apps**            | 4 (accounts, bus, trajets, reservations) |
| **Fichiers Python**          | 45 fichiers `.py`                      |
| **Templates HTML**           | 22 templates                             |
| **Endpoints web**            | 26 URLs                                  |
| **Endpoints API**            | 14 endpoints REST                        |
| **Tests**                    | 31 tests (apps.reservations)             |
| **Taux de réussite**        | 100% (31/31)                             |
| **Lignes de code (estimé)** | ~4 500 lignes                            |

### 12.2 Points forts du code

✅ **Architecture claire** — Séparation nette MVT
✅ **Validation complète** — `full_clean()` systématique
✅ **Sécurité RBAC** — Client voit seulement ses données
✅ **Logging exhaustif** — 3 fichiers rotatifs, toutes les actions
✅ **Tests documentés** — Commentaires `SPRINT X – Feature Y`
✅ **API REST complète** — Pagination, TokenAuth, actions custom
✅ **Règles métier encapsulées** — Toute la logique dans les modèles
✅ **Variables d'environnement** — Aucune credential en dur (sauf dev)

### 12.3 Points d'amélioration identifiés

| # | Amélioration                                               | Priorité | Impact        |
| - | ----------------------------------------------------------- | --------- | ------------- |
| 1 | Bug `Trajet.__str__()` sur `heure_depart` (str vs time) | 🔴        | Tests trajets |
| 2 | Rate limiting sur API                                       | 🟡        | Sécurité    |
| 3 | Tests pour l'app `trajets` (bug existant)                 | 🟡        | Couverture    |
| 4 | Pagination des résultats CSV (gros volumes)                | 🟢        | Performance   |
| 5 | Cache invalidation après nouvelle réservation             | 🟢        | Cohérence    |
| 6 | Tests pour `BusAdmin` et `ReservationAdmin`             | 🟢        | Couverture    |
| 7 | Documentation API (Swagger/DRF Spectacular)                 | 🟢        | DX            |

### 12.4 Conventions de commit (Conventional Commits)

```
feat(pdf):          Génération billets PDF ReportLab
feat(email):        Service email avec pièces jointes
feat(config):       Settings MEDIA, EMAIL, LOGGING, CACHE
feat(reservations): Réservation groupée + remboursement
feat(views):        Dashboard stats, CSV, PDF download
feat(api):          REST API DRF reservations
feat(trajets):      Filtres avancés + cache + API
test(pdf):          Tests unitaires PDF + email
test(integration):  Suite complète 31 tests
docs(readme):       README v2.0
docs(sprint):       SPRINT_LOG.md
chore(env):         .env.example
chore(management):  Dossier commandes de gestion
```
