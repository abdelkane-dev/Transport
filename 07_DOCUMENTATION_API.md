# 🔌 Documentation API REST — Transport Réservation v2.0

> **Framework :** Django REST Framework 3.15.2  
> **Authentification :** Token + Session  
> **Format :** JSON  
> **Base URL :** `http://votre-domaine.com/api/`  
> **Version :** 2.0.0 — Novembre 2024

---

## 📑 Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Authentification](#2-authentification)
3. [API Accounts (Comptes)](#3-api-accounts-comptes)
4. [API Bus](#4-api-bus)
5. [API Trajets](#5-api-trajets)
6. [API Réservations](#6-api-réservations)
7. [Codes de réponse HTTP](#7-codes-de-réponse-http)
8. [Pagination](#8-pagination)
9. [Filtres et recherche](#9-filtres-et-recherche)
10. [Gestion des erreurs](#10-gestion-des-erreurs)
11. [Exemples d'intégration](#11-exemples-dintégration)

---

## 1. Vue d'ensemble

### 1.1 Architecture de l'API

```
/api/
 ├── /accounts/
 │   ├── inscription/      POST   Créer un compte
 │   ├── connexion/        POST   Obtenir un token
 │   ├── deconnexion/      POST   Supprimer le token
 │   └── profil/           GET PUT  Profil utilisateur
 │
 ├── /bus/                 GET POST         Liste / Créer
 │   └── {id}/             GET PUT PATCH DELETE  Détail
 │       └── actifs/       GET              Bus actifs (action custom)
 │
 ├── /trajets/             GET POST         Liste / Créer
 │   └── {id}/             GET PUT PATCH DELETE  Détail
 │       ├── disponibles/  GET              Trajets avec places (caché 5min)
 │       └── filtres/      GET              Filtres avancés
 │
 └── /reservations/        GET POST         Mes réservations / Créer
     └── {id}/             GET PUT PATCH DELETE  Détail
         ├── annuler/      POST             Annuler une réservation
         └── billet/       GET              Télécharger billet PDF
```

### 1.2 Navigateur d'API interactif

Django REST Framework fournit une interface web navigable :

```
http://votre-domaine.com/api/
```

### 1.3 Authentification requise

| Méthode | Usage | Header requis |
|---------|-------|---------------|
| **Token** | Clients API externes | `Authorization: Token <token>` |
| **Session** | Navigateur web | Cookie de session Django |

---

## 2. Authentification

### 2.1 Obtenir un token d'authentification

**Endpoint :** `POST /api/accounts/connexion/`

```bash
curl -X POST http://localhost:8000/api/accounts/connexion/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "motdepasse123"
  }'
```

**Réponse succès (200 OK) :**

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "prenom": "Jean",
    "nom": "Dupont",
    "telephone": "+221771234567"
  }
}
```

**Réponse erreur (400 Bad Request) :**

```json
{
  "non_field_errors": ["Identifiants invalides."]
}
```

### 2.2 Utiliser le token dans les requêtes

Ajoutez le header `Authorization` à toutes vos requêtes :

```bash
# Exemple avec le token
curl -X GET http://localhost:8000/api/reservations/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### 2.3 Créer un compte via API

**Endpoint :** `POST /api/accounts/inscription/`

```bash
curl -X POST http://localhost:8000/api/accounts/inscription/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nouveau@example.com",
    "prenom": "Marie",
    "nom": "Martin",
    "telephone": "+221771234567",
    "password": "MonMotDePasse123",
    "password_confirm": "MonMotDePasse123"
  }'
```

**Réponse succès (201 Created) :**

```json
{
  "message": "Compte créé avec succès.",
  "token": "abc123def456...",
  "user": {
    "id": 5,
    "email": "nouveau@example.com",
    "prenom": "Marie",
    "nom": "Martin"
  }
}
```

### 2.4 Se déconnecter

**Endpoint :** `POST /api/accounts/deconnexion/`

```bash
curl -X POST http://localhost:8000/api/accounts/deconnexion/ \
  -H "Authorization: Token votre-token"
```

**Réponse succès (200 OK) :**

```json
{
  "message": "Déconnexion réussie."
}
```

### 2.5 Voir son profil

**Endpoint :** `GET /api/accounts/profil/`

```bash
curl -X GET http://localhost:8000/api/accounts/profil/ \
  -H "Authorization: Token votre-token"
```

**Réponse (200 OK) :**

```json
{
  "id": 1,
  "email": "user@example.com",
  "prenom": "Jean",
  "nom": "Dupont",
  "telephone": "+221771234567",
  "date_inscription": "2024-11-28T10:00:00Z"
}
```

---

## 3. API Accounts (Comptes)

### Résumé des endpoints

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|:----:|
| `POST` | `/api/accounts/inscription/` | Créer un compte | ❌ |
| `POST` | `/api/accounts/connexion/` | Obtenir un token | ❌ |
| `POST` | `/api/accounts/deconnexion/` | Supprimer le token | ✅ |
| `GET` | `/api/accounts/profil/` | Voir son profil | ✅ |
| `PUT` | `/api/accounts/profil/` | Modifier son profil | ✅ |

### Schéma User (réponse API)

```json
{
  "id": 1,
  "email": "user@example.com",
  "prenom": "Jean",
  "nom": "Dupont",
  "telephone": "+221771234567",
  "date_inscription": "2024-11-28T10:00:00.000Z"
}
```

### Modifier son profil

**Endpoint :** `PUT /api/accounts/profil/`

```bash
curl -X PUT http://localhost:8000/api/accounts/profil/ \
  -H "Authorization: Token votre-token" \
  -H "Content-Type: application/json" \
  -d '{
    "prenom": "Jean-Pierre",
    "nom": "Dupont",
    "telephone": "+221779876543"
  }'
```

---

## 4. API Bus

### 4.1 Résumé des endpoints

| Méthode | Endpoint | Description | Auth | Admin |
|---------|----------|-------------|:----:|:-----:|
| `GET` | `/api/bus/` | Liste tous les bus | ✅ | ❌ |
| `POST` | `/api/bus/` | Créer un bus | ✅ | ✅ |
| `GET` | `/api/bus/{id}/` | Détail d'un bus | ✅ | ❌ |
| `PUT` | `/api/bus/{id}/` | Modifier un bus | ✅ | ✅ |
| `PATCH` | `/api/bus/{id}/` | Modifier partiellement | ✅ | ✅ |
| `DELETE` | `/api/bus/{id}/` | Supprimer un bus | ✅ | ✅ |
| `GET` | `/api/bus/actifs/` | Bus actifs uniquement | ✅ | ❌ |

### 4.2 Schéma Bus (réponse API)

```json
{
  "id": 1,
  "immatriculation": "DK-1234-AB",
  "nombre_places": 50,
  "statut": "ACTIF",
  "statut_libelle": "Actif",
  "est_actif": true,
  "nombre_trajets": 12,
  "notes": "Bus principal ligne Dakar-Thiès",
  "date_creation": "2024-01-01T08:00:00.000Z",
  "date_modification": "2024-11-28T10:00:00.000Z"
}
```

### 4.3 Exemples de requêtes

#### Lister tous les bus

```bash
curl -X GET http://localhost:8000/api/bus/ \
  -H "Authorization: Token votre-token"
```

**Réponse (200 OK) :**

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "immatriculation": "DK-1234-AB",
      "nombre_places": 50,
      "statut": "ACTIF",
      "statut_libelle": "Actif",
      "est_actif": true,
      "nombre_trajets": 12,
      "notes": "",
      "date_creation": "2024-01-01T08:00:00Z",
      "date_modification": "2024-11-28T10:00:00Z"
    }
  ]
}
```

#### Créer un bus (admin requis)

```bash
curl -X POST http://localhost:8000/api/bus/ \
  -H "Authorization: Token votre-token-admin" \
  -H "Content-Type: application/json" \
  -d '{
    "immatriculation": "DK-9999-ZZ",
    "nombre_places": 45,
    "statut": "ACTIF",
    "notes": "Nouveau véhicule acquis en novembre 2024"
  }'
```

**Réponse (201 Created) :**

```json
{
  "id": 6,
  "immatriculation": "DK-9999-ZZ",
  "nombre_places": 45,
  "statut": "ACTIF",
  "statut_libelle": "Actif",
  "est_actif": true,
  "nombre_trajets": 0,
  "notes": "Nouveau véhicule acquis en novembre 2024",
  "date_creation": "2024-11-28T14:30:00Z",
  "date_modification": "2024-11-28T14:30:00Z"
}
```

#### Bus actifs uniquement

```bash
curl -X GET http://localhost:8000/api/bus/actifs/ \
  -H "Authorization: Token votre-token"
```

---

## 5. API Trajets

### 5.1 Résumé des endpoints

| Méthode | Endpoint | Description | Auth | Admin | Cache |
|---------|----------|-------------|:----:|:-----:|:-----:|
| `GET` | `/api/trajets/` | Liste tous les trajets | ✅ | ❌ | ❌ |
| `POST` | `/api/trajets/` | Créer un trajet | ✅ | ✅ | — |
| `GET` | `/api/trajets/{id}/` | Détail d'un trajet | ✅ | ❌ | ❌ |
| `PUT` | `/api/trajets/{id}/` | Modifier un trajet | ✅ | ✅ | — |
| `PATCH` | `/api/trajets/{id}/` | Modifier partiellement | ✅ | ✅ | — |
| `DELETE` | `/api/trajets/{id}/` | Supprimer un trajet | ✅ | ✅ | — |
| `GET` | `/api/trajets/disponibles/` | Trajets avec places dispo | ✅ | ❌ | ✅ 5min |

### 5.2 Schéma Trajet (réponse API)

```json
{
  "id": 1,
  "ville_depart": "Dakar",
  "ville_arrivee": "Thiès",
  "date_depart": "2024-12-01",
  "heure_depart": "08:30:00",
  "prix": "2500.00",
  "prix_formate": "2 500 FCFA",
  "bus": 1,
  "bus_detail": {
    "id": 1,
    "immatriculation": "DK-1234-AB",
    "nombre_places": 50,
    "statut": "ACTIF"
  },
  "places_disponibles": 35,
  "places_reservees": 15,
  "est_complet": false,
  "est_passe": false,
  "taux_remplissage": 30.0,
  "date_creation": "2024-11-25T09:00:00Z",
  "date_modification": "2024-11-28T10:00:00Z"
}
```

### 5.3 Exemples de requêtes

#### Lister les trajets disponibles (avec cache 5min)

```bash
curl -X GET http://localhost:8000/api/trajets/disponibles/ \
  -H "Authorization: Token votre-token"
```

**Réponse (200 OK) :**

```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "ville_depart": "Dakar",
      "ville_arrivee": "Thiès",
      "date_depart": "2024-12-01",
      "heure_depart": "08:30:00",
      "prix_formate": "2 500 FCFA",
      "places_disponibles": 35,
      "est_complet": false
    }
  ]
}
```

#### Lister les trajets avec filtres

```bash
# Filtrer par ville de départ et prix maximum
curl -X GET "http://localhost:8000/api/trajets/?ville_depart=Dakar&prix_max=3000" \
  -H "Authorization: Token votre-token"

# Filtrer par créneau horaire
curl -X GET "http://localhost:8000/api/trajets/?creneau=matin&places_min=2" \
  -H "Authorization: Token votre-token"
```

#### Paramètres de filtre disponibles

| Paramètre | Type | Description | Exemple |
|-----------|------|-------------|---------|
| `ville_depart` | string | Ville de départ (partial match) | `Dakar` |
| `ville_arrivee` | string | Ville d'arrivée (partial match) | `Thies` |
| `date_depart` | date (YYYY-MM-DD) | Date exacte du départ | `2024-12-01` |
| `prix_min` | number | Prix minimum par place | `1000` |
| `prix_max` | number | Prix maximum par place | `5000` |
| `creneau` | string | Créneau horaire | `matin` / `apres_midi` / `soir` / `nuit` |
| `places_min` | integer | Places minimales requises | `2` |
| `exclure_complets` | boolean | Exclure les trajets complets | `true` |

#### Créer un trajet (admin requis)

```bash
curl -X POST http://localhost:8000/api/trajets/ \
  -H "Authorization: Token votre-token-admin" \
  -H "Content-Type: application/json" \
  -d '{
    "bus": 1,
    "ville_depart": "Dakar",
    "ville_arrivee": "Saint-Louis",
    "date_depart": "2024-12-05",
    "heure_depart": "07:00:00",
    "prix": "4500.00"
  }'
```

**Réponse (201 Created) :**

```json
{
  "id": 10,
  "ville_depart": "Dakar",
  "ville_arrivee": "Saint-Louis",
  "date_depart": "2024-12-05",
  "heure_depart": "07:00:00",
  "prix": "4500.00",
  "prix_formate": "4 500 FCFA",
  "bus": 1,
  "places_disponibles": 50,
  "est_complet": false
}
```

---

## 6. API Réservations

### 6.1 Résumé des endpoints

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|:----:|
| `GET` | `/api/reservations/` | Mes réservations | ✅ |
| `POST` | `/api/reservations/` | Créer une réservation | ✅ |
| `GET` | `/api/reservations/{id}/` | Détail d'une réservation | ✅ |
| `PUT` | `/api/reservations/{id}/` | Modifier une réservation | ✅ |
| `PATCH` | `/api/reservations/{id}/` | Modifier partiellement | ✅ |
| `DELETE` | `/api/reservations/{id}/` | Supprimer | ✅ |
| `POST` | `/api/reservations/{id}/annuler/` | Annuler une réservation | ✅ |
| `GET` | `/api/reservations/{id}/billet/` | Télécharger billet PDF | ✅ |

### 6.2 Schéma Réservation (réponse API)

```json
{
  "id": 1,
  "client": 1,
  "client_detail": {
    "id": 1,
    "email": "user@example.com",
    "prenom": "Jean",
    "nom": "Dupont"
  },
  "trajet": 1,
  "trajet_detail": {
    "id": 1,
    "ville_depart": "Dakar",
    "ville_arrivee": "Thiès",
    "date_depart": "2024-12-01",
    "heure_depart": "08:30:00",
    "prix_formate": "2 500 FCFA"
  },
  "nombre_places": 2,
  "date_reservation": "2024-11-28T10:00:00.000Z",
  "statut": "CONFIRMEE",
  "statut_libelle": "Confirmée",
  "prix_total": "5 000 FCFA",
  "peut_etre_annulee": true,
  "notes": ""
}
```

### 6.3 Exemples de requêtes

#### Lister mes réservations

```bash
curl -X GET http://localhost:8000/api/reservations/ \
  -H "Authorization: Token votre-token"
```

**Réponse (200 OK) :**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "trajet_detail": {
        "ville_depart": "Dakar",
        "ville_arrivee": "Thiès",
        "date_depart": "2024-12-01"
      },
      "nombre_places": 2,
      "statut": "CONFIRMEE",
      "prix_total": "5 000 FCFA"
    }
  ]
}
```

#### Créer une réservation

```bash
curl -X POST http://localhost:8000/api/reservations/ \
  -H "Authorization: Token votre-token" \
  -H "Content-Type: application/json" \
  -d '{
    "trajet": 1,
    "nombre_places": 2,
    "notes": "Fenêtre côté gauche si possible"
  }'
```

**Réponse succès (201 Created) :**

```json
{
  "id": 42,
  "client": 1,
  "trajet": 1,
  "trajet_detail": {
    "id": 1,
    "ville_depart": "Dakar",
    "ville_arrivee": "Thiès",
    "date_depart": "2024-12-01",
    "heure_depart": "08:30:00"
  },
  "nombre_places": 2,
  "date_reservation": "2024-11-28T14:30:00Z",
  "statut": "EN_ATTENTE",
  "statut_libelle": "En attente",
  "prix_total": "5 000 FCFA",
  "peut_etre_annulee": true,
  "notes": "Fenêtre côté gauche si possible"
}
```

**Réponse erreur — Trop de places (400 Bad Request) :**

```json
{
  "nombre_places": [
    "Assurez-vous que cette valeur est inférieure ou égale à 10."
  ]
}
```

**Réponse erreur — Plus de places disponibles (400 Bad Request) :**

```json
{
  "non_field_errors": [
    "Pas assez de places disponibles sur ce trajet. Places restantes : 1"
  ]
}
```

#### Annuler une réservation

```bash
curl -X POST http://localhost:8000/api/reservations/42/annuler/ \
  -H "Authorization: Token votre-token" \
  -H "Content-Type: application/json" \
  -d '{
    "raison": "Changement de plans"
  }'
```

**Réponse succès (200 OK) :**

```json
{
  "succes": true,
  "message": "Réservation annulée avec succès.",
  "montant_rembourse": 5000.0,
  "taux_remboursement": 1.0
}
```

**Réponse erreur — Trop tard (400 Bad Request) :**

```json
{
  "succes": false,
  "message": "Annulation impossible : le départ a déjà eu lieu.",
  "montant_rembourse": 0.0
}
```

#### Télécharger le billet PDF

```bash
# Télécharger le billet PDF
curl -X GET http://localhost:8000/api/reservations/42/billet/ \
  -H "Authorization: Token votre-token" \
  --output billet_42.pdf
```

> 📄 La réponse est un fichier binaire PDF (`Content-Type: application/pdf`)

---

## 7. Codes de réponse HTTP

| Code | Statut | Description |
|:----:|--------|-------------|
| `200` | OK | Requête réussie |
| `201` | Created | Ressource créée avec succès |
| `204` | No Content | Suppression réussie |
| `400` | Bad Request | Données invalides (validation échouée) |
| `401` | Unauthorized | Token manquant ou invalide |
| `403` | Forbidden | Accès refusé (pas les droits) |
| `404` | Not Found | Ressource introuvable |
| `405` | Method Not Allowed | Méthode HTTP non supportée |
| `500` | Internal Server Error | Erreur serveur |

---

## 8. Pagination

### 8.1 Configuration par défaut

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20  # 20 résultats par page
}
```

### 8.2 Format de réponse paginée

```json
{
  "count": 55,        // Nombre total de résultats
  "next": "http://localhost:8000/api/reservations/?page=2",
  "previous": null,
  "results": [...]    // Résultats de la page courante
}
```

### 8.3 Naviguer dans les pages

```bash
# Page 1 (défaut)
curl -X GET http://localhost:8000/api/reservations/ \
  -H "Authorization: Token votre-token"

# Page 2
curl -X GET "http://localhost:8000/api/reservations/?page=2" \
  -H "Authorization: Token votre-token"

# Taille de page personnalisée
curl -X GET "http://localhost:8000/api/reservations/?page_size=50" \
  -H "Authorization: Token votre-token"
```

---

## 9. Filtres et recherche

### 9.1 Filtres disponibles par endpoint

#### `/api/trajets/`

| Paramètre | Type | Description |
|-----------|------|-------------|
| `ville_depart` | string | Filtre sur la ville de départ |
| `ville_arrivee` | string | Filtre sur la ville d'arrivée |
| `date_depart` | YYYY-MM-DD | Date exacte du départ |
| `prix_min` | decimal | Prix minimum par place |
| `prix_max` | decimal | Prix maximum par place |
| `creneau` | string | `matin` / `apres_midi` / `soir` / `nuit` |
| `places_min` | integer | Nombre de places minimales requises |
| `exclure_complets` | boolean | Exclure les trajets sans places dispo |

#### `/api/bus/`

| Paramètre | Type | Description |
|-----------|------|-------------|
| `statut` | string | `ACTIF` / `INACTIF` / `MAINTENANCE` |
| `search` | string | Recherche dans l'immatriculation et les notes |

#### `/api/reservations/`

| Paramètre | Type | Description |
|-----------|------|-------------|
| `statut` | string | `EN_ATTENTE` / `CONFIRMEE` / `ANNULEE` |
| `ordering` | string | `-date_reservation` / `trajet__ville_depart` |

### 9.2 Tri des résultats

```bash
# Trier les réservations par date (plus récentes en premier)
curl -X GET "http://localhost:8000/api/reservations/?ordering=-date_reservation" \
  -H "Authorization: Token votre-token"

# Trier les trajets par prix croissant
curl -X GET "http://localhost:8000/api/trajets/?ordering=prix" \
  -H "Authorization: Token votre-token"
```

---

## 10. Gestion des erreurs

### 10.1 Format des erreurs de validation

```json
{
  "champ_concerné": [
    "Message d'erreur"
  ],
  "non_field_errors": [
    "Erreur globale non liée à un champ"
  ]
}
```

### 10.2 Erreurs d'authentification

**Token manquant :**

```json
{
  "detail": "Les informations d'authentification n'ont pas été fournies."
}
```

**Token invalide :**

```json
{
  "detail": "Token invalide."
}
```

**Accès refusé :**

```json
{
  "detail": "Vous n'avez pas la permission d'effectuer cette action."
}
```

### 10.3 Erreurs de validation métier

**Réservation sur trajet complet :**
```json
{"non_field_errors": ["Pas assez de places disponibles sur ce trajet. Places restantes : 0"]}
```

**Annulation déjà annulée :**
```json
{"detail": "Cette réservation est déjà annulée."}
```

**Bus inactif lors de la création d'un trajet :**
```json
{"bus": ["Le bus 'DK-1234-AB' n'est pas ACTIF (statut actuel : En maintenance)."]}
```

---

## 11. Exemples d'intégration

### 11.1 JavaScript (Fetch API)

```javascript
// Configuration de base
const API_BASE = 'http://localhost:8000/api';
const token = localStorage.getItem('auth_token');

const headers = {
  'Authorization': `Token ${token}`,
  'Content-Type': 'application/json'
};

// Lister les trajets disponibles
async function getTrajetsDisponibles() {
  const response = await fetch(`${API_BASE}/trajets/disponibles/`, { headers });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

// Créer une réservation
async function creerReservation(trajetId, nombrePlaces) {
  const response = await fetch(`${API_BASE}/reservations/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      trajet: trajetId,
      nombre_places: nombrePlaces
    })
  });
  
  if (!response.ok) {
    const erreur = await response.json();
    throw new Error(JSON.stringify(erreur));
  }
  
  return response.json();
}

// Annuler une réservation
async function annulerReservation(reservationId, raison = '') {
  const response = await fetch(`${API_BASE}/reservations/${reservationId}/annuler/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ raison })
  });
  return response.json();
}
```

### 11.2 Python (requests)

```python
import requests

API_BASE = 'http://localhost:8000/api'

# Obtenir un token
def get_token(email, password):
    response = requests.post(f'{API_BASE}/accounts/connexion/', json={
        'email': email,
        'password': password
    })
    response.raise_for_status()
    return response.json()['token']

# Client avec authentification
class TransportAPIClient:
    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        })
        self.base_url = API_BASE

    def get_trajets_disponibles(self):
        resp = self.session.get(f'{self.base_url}/trajets/disponibles/')
        resp.raise_for_status()
        return resp.json()

    def creer_reservation(self, trajet_id, nombre_places):
        resp = self.session.post(f'{self.base_url}/reservations/', json={
            'trajet': trajet_id,
            'nombre_places': nombre_places
        })
        resp.raise_for_status()
        return resp.json()

    def telecharger_billet(self, reservation_id, output_path):
        resp = self.session.get(f'{self.base_url}/reservations/{reservation_id}/billet/')
        resp.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        return output_path

# Utilisation
token = get_token('user@example.com', 'motdepasse')
client = TransportAPIClient(token)

trajets = client.get_trajets_disponibles()
print(f"{trajets['count']} trajets disponibles")

reservation = client.creer_reservation(trajet_id=1, nombre_places=2)
print(f"Réservation #{reservation['id']} créée — {reservation['prix_total']}")

client.telecharger_billet(reservation['id'], f"billet_{reservation['id']}.pdf")
```

### 11.3 cURL — Collection complète

```bash
#!/bin/bash
# Script de test complet de l'API

BASE_URL="http://localhost:8000/api"

# 1. Obtenir un token
echo "=== Connexion ==="
TOKEN=$(curl -s -X POST "${BASE_URL}/accounts/connexion/" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"motdepasse"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
echo "Token: ${TOKEN}"

AUTH="Authorization: Token ${TOKEN}"

# 2. Lister les trajets disponibles
echo ""
echo "=== Trajets disponibles ==="
curl -s -X GET "${BASE_URL}/trajets/disponibles/" \
  -H "${AUTH}" | python3 -m json.tool

# 3. Créer une réservation
echo ""
echo "=== Créer une réservation ==="
RESERVATION=$(curl -s -X POST "${BASE_URL}/reservations/" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d '{"trajet": 1, "nombre_places": 1}')
echo "${RESERVATION}" | python3 -m json.tool
RESA_ID=$(echo "${RESERVATION}" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 4. Annuler la réservation
echo ""
echo "=== Annuler la réservation #${RESA_ID} ==="
curl -s -X POST "${BASE_URL}/reservations/${RESA_ID}/annuler/" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d '{"raison":"Test API"}' | python3 -m json.tool

echo ""
echo "=== Tests terminés ==="
```

---

<div align="center">

*[← Guide Administrateur](06_GUIDE_ADMINISTRATEUR.md) • [Changelog →](08_CHANGELOG.md)*

</div>
