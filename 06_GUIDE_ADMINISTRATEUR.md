# 🔧 Guide Administrateur — Transport Réservation v2.0

> **Application de réservation de billets de bus**  
> **Audience :** Administrateurs système et gestionnaires  
> **Version :** 2.0.0 — Novembre 2024  
> **Accès requis :** Compte avec `is_staff = True`

---

## 📑 Table des matières

1. [Accès administrateur](#1-accès-administrateur)
2. [Interface d'administration Django](#2-interface-dadministration-django)
3. [Gestion de la flotte de bus](#3-gestion-de-la-flotte-de-bus)
4. [Gestion des trajets](#4-gestion-des-trajets)
5. [Gestion des réservations](#5-gestion-des-réservations)
6. [Gestion des utilisateurs](#6-gestion-des-utilisateurs)
7. [Monitoring et logs](#7-monitoring-et-logs)
8. [Gestion du cache](#8-gestion-du-cache)
9. [Actions en masse](#9-actions-en-masse)
10. [Interface HTML admin](#10-interface-html-admin)
11. [Commandes de maintenance](#11-commandes-de-maintenance)
12. [Sécurité et RBAC](#12-sécurité-et-rbac)

---

## 1. Accès administrateur

### 1.1 Niveaux d'accès

| Niveau | Champ | Accès |
|--------|-------|-------|
| **Client** | `is_staff = False` | Dashboard personnel, ses réservations uniquement |
| **Staff Admin** | `is_staff = True` | Gestion bus, trajets, tous les utilisateurs |
| **Super Admin** | `is_superuser = True` | Interface Django Admin complète |

### 1.2 Créer un compte administrateur

```bash
# Via la ligne de commande
python manage.py createsuperuser
# → Renseigner : email, prénom, nom, mot de passe

# Promouvoir un utilisateur existant en admin
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(email='admin@example.com')
u.is_staff = True
u.is_superuser = True
u.save()
print('Admin créé :', u.email)
"
```

### 1.3 URLs d'accès

| Interface | URL | Accès requis |
|-----------|-----|:------------:|
| Interface admin Django | `/admin/` | `is_superuser` |
| Gestion bus HTML | `/bus/` | Lecture : tous \| Écriture : `is_staff` |
| Gestion trajets HTML | `/trajets/` | Lecture : tous \| Écriture : `is_staff` |
| API REST admin | `/api/` | Token + `is_staff` |

---

## 2. Interface d'administration Django

### 2.1 Accès

```
URL : http://votre-domaine.com/admin/
```

Connexion avec les identifiants **superutilisateur** (email + mot de passe).

### 2.2 Personnalisation du panneau d'administration

L'interface admin a été personnalisée avec :

```python
admin.site.site_header = "Transport Réservation – Administration"
admin.site.site_title  = "Transport Admin"
admin.site.index_title = "Tableau de bord administrateur"
```

### 2.3 Modules disponibles dans l'admin

| Module | Modèle | Description |
|--------|--------|-------------|
| **Accounts** | `User` | Gestion des comptes utilisateurs |
| **Bus** | `Bus` | Gestion de la flotte de véhicules |
| **Trajets** | `Trajet` | Gestion des trajets (itinéraires) |
| **Reservations** | `Reservation` | Suivi de toutes les réservations |
| **Auth** | `Token` | Tokens d'authentification API |

---

## 3. Gestion de la flotte de bus

### 3.1 Modèle Bus — Champs disponibles

| Champ | Type | Description | Contraintes |
|-------|------|-------------|-------------|
| `immatriculation` | CharField | Numéro d'immatriculation | Unique, format libre |
| `nombre_places` | PositiveIntegerField | Capacité totale | > 0 |
| `statut` | CharField | État du véhicule | ACTIF / INACTIF / MAINTENANCE |
| `notes` | TextField | Notes internes | Optionnel |
| `date_creation` | DateTimeField | Date d'ajout | Auto (lecture seule) |
| `date_modification` | DateTimeField | Dernière modification | Auto (lecture seule) |

> ⚠️ **Important :** Le modèle Bus ne contient PAS de champs `marque` ou `modele`. Ces informations peuvent être intégrées dans le champ `notes`.

### 3.2 Statuts des bus

| Statut | Couleur | Description | Impact sur les trajets |
|--------|:-------:|-------------|----------------------|
| `ACTIF` | 🟢 Vert | Bus opérationnel | Peut être assigné à des trajets |
| `INACTIF` | ⚫ Gris | Bus retiré du service | Non assignable à de nouveaux trajets |
| `MAINTENANCE` | 🟡 Orange | Bus en révision | Non assignable temporairement |

### 3.3 Créer un nouveau bus

#### Via l'interface HTML (`/bus/creer/` — admin requis)

1. Naviguer vers `/bus/`
2. Cliquer sur **"+ Ajouter un bus"** (visible uniquement si `is_staff`)
3. Remplir le formulaire :
   - **Immatriculation** : `DK-1234-AB`
   - **Nombre de places** : `50`
   - **Statut** : `ACTIF`
   - **Notes** : `Acheté le 01/01/2024, révision prévue...`
4. Cliquer sur **"Enregistrer"**

#### Via l'API REST

```bash
curl -X POST http://localhost:8000/api/bus/ \
  -H "Authorization: Token votre-token-admin" \
  -H "Content-Type: application/json" \
  -d '{
    "immatriculation": "DK-5678-EF",
    "nombre_places": 50,
    "statut": "ACTIF",
    "notes": "Nouveau véhicule"
  }'
```

### 3.4 Actions en masse sur les bus

Depuis l'interface admin (`/admin/bus/bus/`), sélectionnez plusieurs bus et appliquez :

| Action | Description |
|--------|-------------|
| ✅ **Marquer comme ACTIF** | Remet en service les bus sélectionnés |
| 🔧 **Mettre en MAINTENANCE** | Place les bus en maintenance |
| ❌ **Marquer comme INACTIF** | Retire les bus du service |

### 3.5 Filtres et recherche bus

| Filtre | Valeurs | Usage |
|--------|---------|-------|
| **Recherche texte** | immatriculation, notes | Barre de recherche |
| **Statut** | ACTIF / INACTIF / MAINTENANCE | Filtre latéral |
| **Date création** | Hiérarchie par date | Navigation temporelle |

```
URL filtrée : /bus/?statut=ACTIF
```

---

## 4. Gestion des trajets

### 4.1 Modèle Trajet — Champs

| Champ | Type | Description |
|-------|------|-------------|
| `bus` | ForeignKey | Bus assigné (clé étrangère) |
| `ville_depart` | CharField | Ville de départ |
| `ville_arrivee` | CharField | Ville d'arrivée |
| `date_depart` | DateField | Date du départ |
| `heure_depart` | TimeField | Heure du départ |
| `prix` | DecimalField | Prix par place (FCFA) |
| `date_creation` | DateTimeField | Auto |
| `date_modification` | DateTimeField | Auto |

### 4.2 Calcul des places disponibles

La méthode `places_disponibles()` calcule en temps réel le nombre de places libres :

```
Places disponibles = Bus.nombre_places - Σ(reservations actives confirmées)
```

### 4.3 Créer un trajet

#### Via l'interface HTML (`/trajets/creer/` — admin requis)

1. Naviguer vers `/trajets/`
2. Cliquer sur **"+ Nouveau trajet"** (visible uniquement si `is_staff`)
3. Remplir le formulaire :

| Champ | Exemple |
|-------|---------|
| Bus | Sélectionner `DK-1234-AB (50 places)` |
| Ville de départ | `Dakar` |
| Ville d'arrivée | `Thiès` |
| Date de départ | `2024-12-01` |
| Heure de départ | `08:30` |
| Prix par place | `2500` |

4. Valider avec **"Enregistrer le trajet"**

#### Via l'API REST

```bash
curl -X POST http://localhost:8000/api/trajets/ \
  -H "Authorization: Token votre-token-admin" \
  -H "Content-Type: application/json" \
  -d '{
    "bus": 1,
    "ville_depart": "Dakar",
    "ville_arrivee": "Thiès",
    "date_depart": "2024-12-01",
    "heure_depart": "08:30:00",
    "prix": "2500.00"
  }'
```

### 4.4 Modifier/Supprimer un trajet

> ⚠️ **Attention :** La suppression d'un trajet avec des réservations actives est protégée au niveau de la base de données. Annulez d'abord toutes les réservations associées.

```
Modifier : /trajets/{id}/modifier/   (admin requis)
Supprimer : /trajets/{id}/supprimer/ (admin requis)
```

---

## 5. Gestion des réservations

### 5.1 Vue d'ensemble des réservations (Admin)

L'interface admin (`/admin/reservations/reservation/`) offre une vue complète de toutes les réservations :

| Colonne | Description |
|---------|-------------|
| ID | Numéro unique de réservation |
| Client | Nom complet du voyageur |
| Trajet | Résumé : Départ → Arrivée (date) |
| Places | Nombre de places réservées |
| Prix total | Montant calculé automatiquement |
| Statut | Badge coloré (EN_ATTENTE / CONFIRMÉE / ANNULÉE) |
| Date | Date de création de la réservation |

### 5.2 Cycle de vie d'une réservation

```
[CRÉATION] ──► EN_ATTENTE ──► CONFIRMÉE ──► ─────────
                    │                          │
                    └──────── ANNULÉE ◄─────────┘
```

### 5.3 Actions d'administration sur les réservations

| Action | Description | Condition |
|--------|-------------|-----------|
| ✅ **Confirmer** | Valide les réservations EN_ATTENTE | Statut = EN_ATTENTE |
| ❌ **Annuler** | Annule les réservations sélectionnées | Statut ≠ ANNULÉE |

#### Procédure de confirmation en masse

1. Dans `/admin/reservations/reservation/`
2. Sélectionner les réservations EN_ATTENTE (cocher les cases)
3. Dans "Action", sélectionner **"✅ Confirmer les réservations sélectionnées"**
4. Cliquer sur **"Exécuter"**

### 5.4 Filtres de recherche réservations

| Type de filtre | Options |
|----------------|---------|
| Recherche texte | Nom client, prénom, email, ville départ/arrivée |
| Statut | EN_ATTENTE / CONFIRMEE / ANNULEE |
| Date réservation | Hiérarchie par date |
| Ville de départ | Liste des villes |

### 5.5 Export des réservations

**Via l'interface admin HTML** (accès staff) :
```
/reservations/export/csv/
```

**Via API REST** :
```bash
# Export des réservations d'un utilisateur spécifique
curl -X GET "http://localhost:8000/api/reservations/?format=json" \
  -H "Authorization: Token votre-token"
```

---

## 6. Gestion des utilisateurs

### 6.1 Modèle User personnalisé

Le modèle `User` étend `AbstractUser` avec les champs supplémentaires :

| Champ | Type | Description |
|-------|------|-------------|
| `email` | EmailField | **Identifiant de connexion** (USERNAME_FIELD) |
| `prenom` | CharField | Prénom |
| `nom` | CharField | Nom de famille |
| `telephone` | CharField | Numéro de téléphone |
| `date_inscription` | DateTimeField | Date de création du compte (auto) |
| `is_staff` | BooleanField | Accès admin |
| `is_superuser` | BooleanField | Accès superadmin |

### 6.2 Promouvoir un utilisateur

#### Via l'interface admin

1. Aller dans `/admin/accounts/user/`
2. Cliquer sur l'utilisateur à promouvoir
3. Dans la section **"Autorisations"** :
   - Cocher **"Statut équipe"** → `is_staff = True`
   - Cocher **"Statut super-utilisateur"** → `is_superuser = True`
4. Sauvegarder

#### Via la commande shell

```bash
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(email='gestionnaire@transport.com')
u.is_staff = True
u.save()
print(f'Utilisateur {u.email} promu gestionnaire.')
"
```

### 6.3 Réinitialiser le mot de passe d'un utilisateur

```bash
python manage.py changepassword user@example.com
```

### 6.4 Token API d'un utilisateur

```bash
python manage.py shell -c "
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(email='user@example.com')
token, created = Token.objects.get_or_create(user=u)
print(f'Token: {token.key}')
"
```

---

## 7. Monitoring et logs

### 7.1 Configuration des logs

L'application génère 3 fichiers de logs dans le dossier `logs/` :

| Fichier | Handler | Contenu | Taille max | Archives |
|---------|---------|---------|:----------:|:--------:|
| `transport.log` | `RotatingFileHandler` | Logs généraux (INFO+) | 5 Mo | 5 |
| `errors.log` | `RotatingFileHandler` | Erreurs uniquement (ERROR+) | 5 Mo | 5 |
| `reservations.log` | `RotatingFileHandler` | Logs réservations (DEBUG+) | 5 Mo | 5 |

### 7.2 Consulter les logs en temps réel

```bash
# Logs généraux
tail -f logs/transport.log

# Erreurs uniquement
tail -f logs/errors.log

# Activité réservations
tail -f logs/reservations.log

# Rechercher dans les logs
grep "ANNULATION" logs/reservations.log
grep "ERROR" logs/errors.log | tail -50
```

### 7.3 Format des messages de log

```
2024-11-28 10:30:45,123 INFO     transport.reservations - CRÉATION réservation #42 : user@email.com, trajet #5 (Dakar→Thiès), 2 places
2024-11-28 10:31:02,456 INFO     transport.reservations - ANNULATION réservation #38 : user@email.com, motif: Voyage annulé, remboursement: 2500.00 FCFA
2024-11-28 10:35:00,789 ERROR    transport.errors       - Erreur PDF génération : [détail de l'erreur]
```

### 7.4 Rotation automatique des logs

Les logs sont automatiquement archivés quand ils atteignent 5 Mo :
- `transport.log` → `transport.log.1`, `.log.2`, ..., `.log.5`
- Les archives au-delà de 5 sont supprimées automatiquement

---

## 8. Gestion du cache

### 8.1 Cache des trajets disponibles

L'endpoint `/api/trajets/disponibles/` utilise un cache avec TTL de 300 secondes :

```python
cache_key = 'api_trajets_disponibles'
# Cache invalidé après 5 minutes OU manuellement
```

### 8.2 Invalidation manuelle du cache

```bash
# Via le shell Django
python manage.py shell -c "
from django.core.cache import cache
cache.delete('api_trajets_disponibles')
print('Cache invalidé avec succès')
"

# Tout vider (avec précaution en production)
python manage.py shell -c "
from django.core.cache import cache
cache.clear()
print('Tout le cache a été vidé')
"
```

### 8.3 Configuration Redis (production)

Pour activer Redis en production, définir la variable d'environnement :

```bash
# .env ou variable d'environnement
REDIS_URL=redis://localhost:6379/0

# Installer django-redis
pip install django-redis==5.4.0 redis==5.0.7
```

Puis décommenter dans `requirements.txt` :

```
django-redis==5.4.0
redis==5.0.7
```

### 8.4 Vérifier l'état du cache

```bash
# En développement (LocMemCache)
python manage.py shell -c "
from django.core.cache import cache
val = cache.get('api_trajets_disponibles')
print('Cache présent :', val is not None)
if val: print('Nombre de trajets cachés :', len(val))
"
```

---

## 9. Actions en masse

### 9.1 Résumé des actions disponibles

| Module | Action | Description |
|--------|--------|-------------|
| Bus | ✅ Marquer ACTIF | Remet en service |
| Bus | 🔧 Marquer MAINTENANCE | Mise en révision |
| Bus | ❌ Marquer INACTIF | Retire du service |
| Réservations | ✅ Confirmer | Valide les EN_ATTENTE |
| Réservations | ❌ Annuler | Annule les sélectionnées |

### 9.2 Procédure générale pour les actions en masse

1. Aller dans l'interface admin (`/admin/`)
2. Naviguer vers le module souhaité
3. Cocher les éléments à traiter
4. Sélectionner l'action dans le menu déroulant **"Action"**
5. Cliquer sur **"Exécuter"**
6. Lire le message de confirmation

---

## 10. Interface HTML admin

### 10.1 URLs HTML réservées aux administrateurs (`is_staff`)

Ces URLs sont accessibles via le navigateur mais nécessitent `is_staff = True` :

| URL | Description |
|-----|-------------|
| `/bus/creer/` | Ajouter un bus à la flotte |
| `/bus/{id}/modifier/` | Modifier les données d'un bus |
| `/bus/{id}/supprimer/` | Supprimer un bus |
| `/trajets/creer/` | Créer un nouveau trajet |
| `/trajets/{id}/modifier/` | Modifier un trajet |
| `/trajets/{id}/supprimer/` | Supprimer un trajet |

### 10.2 Gestion d'un bus via l'interface HTML

#### Liste des bus avec filtres

```
/bus/?statut=ACTIF       → Bus actifs uniquement
/bus/?statut=MAINTENANCE → Bus en maintenance
/bus/                    → Tous les bus
```

#### Tableau de la liste buses

```
┌──────────────────────────────────────────────────────────────┐
│  Immatricul.  │ Places │   Statut    │ Trajets │  Créé le    │
│──────────────────────────────────────────────────────────────│
│  DK-1234-AB   │   50   │ ● ACTIF     │   12    │ 01/01/2024  │
│  DK-5678-CD   │   45   │ ● MAINTENAN.│    8    │ 15/03/2024  │
│  DK-9012-EF   │   30   │ ● INACTIF   │    0    │ 20/06/2024  │
└──────────────────────────────────────────────────────────────┘
```

---

## 11. Commandes de maintenance

### 11.1 Commandes Django courantes

```bash
# Vérifier la configuration (doit retourner 0 erreurs)
python manage.py check

# Vérifier les migrations en attente
python manage.py showmigrations

# Appliquer toutes les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Nettoyer les sessions expirées
python manage.py clearsessions
```

### 11.2 Nettoyage des tokens API expirés

```bash
python manage.py shell -c "
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()
# Afficher les tokens actifs
count = Token.objects.count()
print(f'Tokens actifs : {count}')
"
```

### 11.3 Statistiques de la base de données

```bash
python manage.py shell -c "
from apps.bus.models import Bus
from apps.trajets.models import Trajet
from apps.reservations.models import Reservation
from django.contrib.auth import get_user_model
User = get_user_model()

print('=== STATISTIQUES ===')
print(f'Bus total       : {Bus.objects.count()}')
print(f'Bus actifs      : {Bus.objects.filter(statut=\"ACTIF\").count()}')
print(f'Trajets total   : {Trajet.objects.count()}')
print(f'Réservations    : {Reservation.objects.count()}')
print(f'  EN_ATTENTE    : {Reservation.objects.filter(statut=\"EN_ATTENTE\").count()}')
print(f'  CONFIRMEES    : {Reservation.objects.filter(statut=\"CONFIRMEE\").count()}')
print(f'  ANNULEES      : {Reservation.objects.filter(statut=\"ANNULEE\").count()}')
print(f'Utilisateurs    : {User.objects.count()}')
print(f'Admins          : {User.objects.filter(is_staff=True).count()}')
"
```

### 11.4 Sauvegarde de la base de données

```bash
# SQLite (développement)
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)

# Dump JSON de toutes les données
python manage.py dumpdata --indent=2 > backup_$(date +%Y%m%d).json

# Restaurer depuis un dump
python manage.py loaddata backup_YYYYMMDD.json
```

---

## 12. Sécurité et RBAC

### 12.1 Modèle de contrôle d'accès (RBAC)

```
┌─────────────────────────────────────────────────────────────┐
│                    RÔLES ET PERMISSIONS                      │
│                                                             │
│  Visiteur (non connecté)                                    │
│  ├── Voir la liste des trajets                              │
│  ├── Voir le détail d'un trajet                             │
│  └── Inscription / Connexion                                │
│                                                             │
│  Client (is_staff = False)                                  │
│  ├── Tout ce que Visiteur peut faire                        │
│  ├── Réserver un trajet                                     │
│  ├── Voir SES PROPRES réservations uniquement               │
│  ├── Annuler SES PROPRES réservations                       │
│  ├── Télécharger SES PROPRES billets                        │
│  └── Exporter SES PROPRES données CSV                       │
│                                                             │
│  Staff Admin (is_staff = True)                              │
│  ├── Tout ce que Client peut faire                          │
│  ├── Créer/Modifier/Supprimer des bus                       │
│  ├── Créer/Modifier/Supprimer des trajets                   │
│  └── Voir toutes les réservations (via admin)               │
│                                                             │
│  Super Admin (is_superuser = True)                          │
│  └── Accès complet à tout (interface admin Django)          │
└─────────────────────────────────────────────────────────────┘
```

### 12.2 Isolation des données client

**Principe d'isolation :** Un client ne peut JAMAIS voir les réservations d'un autre client.

La vue `DashboardView` filtre systématiquement :
```python
# apps/reservations/views.py
def get_queryset(self):
    return Reservation.objects.filter(
        client=self.request.user  # ← Isolation stricte
    ).select_related('trajet', 'trajet__bus')
```

De même pour le billet PDF :
```python
# Vérification propriétaire du billet
if reservation.client != request.user:
    return HttpResponseForbidden("Accès refusé.")
```

### 12.3 Validation des données

Toutes les modifications passent par `full_clean()` avant sauvegarde :
- `MaxValueValidator(10)` sur `Reservation.nombre_places`
- Vérification de disponibilité avant création de réservation
- Email unique pour chaque utilisateur

### 12.4 Protection CSRF

Tous les formulaires Django incluent le token CSRF automatiquement via `{% csrf_token %}`.

### 12.5 Checklist de sécurité (production)

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` longue et aléatoire (50+ caractères)
- [ ] `ALLOWED_HOSTS` restreint aux domaines réels
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `X_FRAME_OPTIONS = 'DENY'`
- [ ] `SECURE_HSTS_SECONDS = 31536000`
- [ ] Base de données PostgreSQL (pas SQLite)
- [ ] Logs en dehors du répertoire web

---

<div align="center">

*[← Guide Utilisateur](05_GUIDE_UTILISATEUR.md) • [Documentation API →](07_DOCUMENTATION_API.md)*

</div>
