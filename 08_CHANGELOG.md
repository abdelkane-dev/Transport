# 📝 Changelog — Transport Réservation

> Toutes les modifications notables de ce projet sont documentées ici.  
> Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)  
> Versioning : [Semantic Versioning](https://semver.org/lang/fr/)

---

## [2.0.0] — 2024-11-21 — Version complète (12 features)

> 🏷️ Tag Git : `v2.0.0` — Commit : `2ed680e`  
> 🎯 Sprints complétés : Sprint 1, 2, 3, 4

### 🚀 Ajouté — Sprint 4 (21 Nov 2024)

#### Feature 9 — API REST complète

- `feat(api)` : ViewSets DRF pour Bus, Trajet, Reservation, Accounts
- `feat(api)` : Pagination par numéro de page (20 résultats par défaut)
- `feat(api)` : Actions personnalisées : `disponibles/`, `actifs/`, `annuler/`, `billet/`
- `feat(api)` : Authentification Token + Session simultanée
- `feat(api)` : Permissions `IsAuthenticated` pour clients, `IsAdminUser` pour opérations admin
- `feat(api)` : Serializers complets avec champs calculés (prix_total, places_disponibles, taux_remplissage)
- `feat(api)` : Validation métier dans les serializers (full_clean, règles bus actif)
- `feat(api)` : Endpoints : `/api/accounts/`, `/api/bus/`, `/api/trajets/`, `/api/reservations/`

#### Feature 10 — Logging structuré

- `feat(logging)` : 3 RotatingFileHandlers : `transport.log`, `errors.log`, `reservations.log`
- `feat(logging)` : Rotation automatique à 5 Mo, conservation de 5 archives
- `feat(logging)` : Loggers nommés : `transport`, `transport.reservations`, `transport.errors`
- `feat(logging)` : Logging des créations, annulations, téléchargements de billets
- `feat(logging)` : Logging des erreurs PDF et email
- `feat(logging)` : Format : `timestamp - level - logger - message`

#### Feature 11 — Cache Redis

- `feat(cache)` : Cache LocMemCache (développement) — configuration automatique
- `feat(cache)` : Cache Redis (production) — activé via `REDIS_URL` dans `.env`
- `feat(cache)` : Cache de l'endpoint `/api/trajets/disponibles/` avec TTL=300s
- `feat(cache)` : Clé de cache : `api_trajets_disponibles`
- `feat(cache)` : Cache hit/miss transparent pour le client API

#### Feature 12 — RBAC et isolation des données

- `feat(security)` : Isolation stricte : clients voient uniquement leurs propres réservations
- `feat(security)` : Mixin `AdminRequiredMixin` pour opérations sensibles (bus, trajets CRUD)
- `feat(security)` : Vérification propriétaire billet PDF : `HttpResponseForbidden` si accès non autorisé
- `feat(security)` : API : filtrage automatique par `request.user` dans `get_queryset()`

### 🔧 Amélioré — Sprint 4

- `refactor(api)` : Centralisation des permissions DRF dans les ViewSets
- `refactor(settings)` : Configuration LOGGING complète dans `settings.py`
- `docs(sprint)` : `SPRINT_LOG.md` — journal DevOps des 4 sprints

---

## [1.5.0] — 2024-11-20 à 21 — Sprint 3 complet

> 🎯 Sprint 3 : Annulation remboursée, Filtres avancés, Notifications

### 🚀 Ajouté — Sprint 3

#### Feature 6 — Annulation avec remboursement simulé

- `feat(reservation)` : Méthode `peut_etre_annulee_avec_remboursement()` → retourne `(bool, float, str)`
- `feat(reservation)` : Méthode `annuler()` → retourne tuple `(bool, str, float)`
- `feat(reservation)` : Règle remboursement : `taux=1.0` si >24h avant départ
- `feat(reservation)` : Règle remboursement : `taux=0.5` si entre 2h et 24h
- `feat(reservation)` : Règle remboursement : `taux=0.0` si <2h avant départ
- `feat(reservation)` : Vue `AnnulationView` avec affichage du taux estimé avant confirmation
- `feat(reservation)` : `AnnulationForm` avec champ `raison` optionnel

#### Feature 7 — Filtres avancés sur les trajets

- `feat(trajets)` : Filtre `prix_min` — prix minimum par place
- `feat(trajets)` : Filtre `prix_max` — prix maximum par place
- `feat(trajets)` : Filtre `creneau` — créneaux horaires (matin/apres_midi/soir/nuit)
- `feat(trajets)` : Filtre `places_min` — nombre de places minimales requises
- `feat(trajets)` : Filtre `exclure_complets` — masquer les trajets sans places
- `feat(trajets)` : Formulaire `FiltresAvancesTrajetForm` avec widgets adaptés
- `feat(trajets)` : Constante `CRENEAUX_HEURES` définissant les plages horaires

#### Feature 8 — Notifications système enrichies

- `feat(notifications)` : Messages Django enrichis à chaque action (réservation, annulation)
- `feat(notifications)` : Message succès réservation avec montant total
- `feat(notifications)` : Message annulation avec montant de remboursement estimé
- `feat(notifications)` : Message d'erreur si places insuffisantes
- `feat(notifications)` : Badge de statut coloré dans les templates

### 🔧 Amélioré — Sprint 3

- `refactor(forms)` : Ajout de `AdminReservationForm` pour usage admin
- `refactor(templates)` : Intégration des filtres avancés dans `trajet_liste.html`

---

## [1.2.0] — 2024-11-19 à 20 — Sprint 2 complet

> 🎯 Sprint 2 : Dashboard stats + Export CSV

### 🚀 Ajouté — Sprint 2

#### Feature 4 — Statistiques graphiques (Dashboard)

- `feat(stats)` : Vue `dashboard_stats_view()` avec données Chart.js
- `feat(stats)` : Graphique barres : dépenses mensuelles (`TruncMonth`)
- `feat(stats)` : Graphique camembert : trajets par destination populaire
- `feat(stats)` : Calcul des totaux dépensés par utilisateur
- `feat(stats)` : Serialisation JSON sécurisée avec `json.dumps()`
- `feat(stats)` : Route `/reservations/stats/`

#### Feature 5 — Export CSV

- `feat(csv)` : Vue `export_csv_view()` — export des réservations utilisateur
- `feat(csv)` : Encodage UTF-8 BOM (compatible Excel, LibreOffice)
- `feat(csv)` : 12 colonnes : Référence, Trajet, Date réservation, Date départ, Heure, Ville départ, Ville arrivée, Places, Prix unitaire, Prix total, Statut, Raison annulation
- `feat(csv)` : Nom de fichier dynamique : `reservations_{email}_{date}.csv`
- `feat(csv)` : Route `/reservations/export/csv/`

### 🔧 Amélioré — Sprint 2

- `refactor(dashboard)` : Ajout des statistiques dans le contexte `DashboardView`
- `feat(dashboard)` : Calcul total dépensé pour réservations actives

---

## [1.0.0] — 2024-11-18 à 19 — Version initiale (Sprint 1)

> 🏷️ Tag Git : `v1.0.0` — Commit : `53cab66`  
> 🎯 Sprint 1 : Fonctionnalités de base + PDF + Email + Dashboard

### 🚀 Ajouté — Sprint 1

#### Socle technique (chore/feat de base)

- `chore(init)` : Initialisation du projet Django 5.1.4
- `chore(init)` : Structure 4 applications : accounts, bus, trajets, reservations
- `chore(init)` : Configuration `AUTH_USER_MODEL = 'accounts.User'`
- `chore(init)` : `email` comme `USERNAME_FIELD` dans le modèle User
- `chore(deps)` : Installation des dépendances : DRF, ReportLab, qrcode, Pillow, Whitenoise, Gunicorn
- `feat(models)` : Modèle `Bus` — immatriculation, nombre_places, statut (ACTIF/INACTIF/MAINTENANCE)
- `feat(models)` : Modèle `Trajet` — FK Bus, villes, date/heure départ, prix
- `feat(models)` : Modèle `Reservation` — FK User+Trajet, places (max 10), statut, date
- `feat(models)` : Modèle `User` — extension AbstractUser avec prenom, nom, telephone
- `feat(admin)` : `BusAdmin` avec badge_statut coloré et actions en masse
- `feat(admin)` : `ReservationAdmin` avec confirmer/annuler en masse
- `feat(views)` : `DashboardView` (CBV ListView) avec isolation client
- `feat(views)` : `TrajetListeView` avec filtres de base
- `feat(views)` : `ReservationCreerView` — création avec validation

#### Feature 1 — Génération de billets PDF

- `feat(pdf)` : Classe `BilletPDFGenerator` utilisant ReportLab 4.2.2
- `feat(pdf)` : Template PDF : en-tête, détails trajet, QR code, pied de page
- `feat(pdf)` : Génération QR code via `qrcode[pil] 8.0` en mémoire (`io.BytesIO`)
- `feat(pdf)` : Styles : `ParagraphStyle` avec `textColor=COULEUR_*` (pas inline `<font>`)
- `feat(pdf)` : Vue `telecharger_billet_view()` — HttpResponse avec Content-Type PDF
- `feat(pdf)` : Route `/reservations/{id}/billet/`

#### Feature 2 — Service d'email

- `feat(email)` : Classe `EmailBilletService` avec méthodes `envoyer_confirmation()` et `envoyer_annulation()`
- `feat(email)` : Email de confirmation : billet en pièce jointe PDF
- `feat(email)` : Email d'annulation : résumé et montant remboursé
- `feat(email)` : Backend console (développement) / SMTP configurable (production)
- `feat(email)` : Gestion des erreurs d'envoi sans interruption du flux

#### Feature 3 — Dashboard client

- `feat(dashboard)` : Vue `DashboardView` — liste paginée (10/page) des réservations
- `feat(dashboard)` : Compteurs : total, actives, annulées
- `feat(dashboard)` : Filtre strict `filter(client=request.user)` — isolation des données
- `feat(dashboard)` : Route `/reservations/dashboard/`

---

## [0.1.0] — 2024-11-18 — Initialisation du dépôt

### 🚀 Ajouté

- `chore(init)` : `git init` — Initialisation du dépôt Git
- `chore(init)` : `.gitignore` Django/Python (venv, .env, __pycache__, *.pyc, db.sqlite3, media, logs)
- `chore(init)` : `README.md` initial
- `chore(init)` : Structure de dossiers de base

---

## Légende

| Type de commit | Emoji | Description |
|---------------|:-----:|-------------|
| `feat` | ✨ | Nouvelle fonctionnalité |
| `fix` | 🐛 | Correction de bug |
| `docs` | 📚 | Documentation |
| `chore` | 🔧 | Tâches de maintenance |
| `refactor` | ♻️ | Refactoring sans nouvelle feature |
| `test` | ✅ | Ajout ou modification de tests |
| `perf` | ⚡ | Amélioration des performances |
| `security` | 🔒 | Amélioration de la sécurité |

---

## Comparaison des versions

| Version | Features | Tests | API | Cache | Logs |
|---------|:--------:|:-----:|:---:|:-----:|:----:|
| `0.1.0` | 0 | 0 | ❌ | ❌ | ❌ |
| `1.0.0` | 3 | ~10 | ❌ | ❌ | ❌ |
| `1.2.0` | 5 | ~20 | ❌ | ❌ | ❌ |
| `1.5.0` | 8 | ~28 | ❌ | ❌ | ❌ |
| `2.0.0` | 12 | 31 | ✅ | ✅ | ✅ |

---

<div align="center">

*[← Documentation API](07_DOCUMENTATION_API.md) • [Guide Contribution →](09_GUIDE_CONTRIBUTION.md)*

</div>
