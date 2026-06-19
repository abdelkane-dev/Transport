# 🐛 RAPPORT D'ANOMALIES — Transport Réservation v2.0

> **Projet :** Application de réservation de billets de bus
> **Rôle :** Assistant QA & Documentation
> **Version :** v2.0.0 — Sprint 4
> **Date :** Juin 2025

---

## 📊 Résumé exécutif

| Sévérité     | Nombre      | Résolues   | En cours    | Ouvertes    |
| --------------- | ----------- | ----------- | ----------- | ----------- |
| 🔴 Critique     | 2           | 2           | 0           | 0           |
| 🟠 Majeure      | 1           | 0           | 0           | 1           |
| 🟡 Mineure      | 2           | 0           | 0           | 2           |
| 🟢 Triviale     | 1           | 0           | 0           | 1           |
| **Total** | **6** | **2** | **0** | **4** |

---

## BUG-001 — ✅ RÉSOLU : Champs inexistants dans le helper de test

| Champ                           | Valeur                                                                 |
| ------------------------------- | ---------------------------------------------------------------------- |
| **ID**                    | BUG-001                                                                |
| **Titre**                 | `Bus()` called with inexistent fields `marque` and `modele`      |
| **Sévérité**           | 🔴 Critique                                                            |
| **Sprint détecté**      | Sprint 4 — lors de l'exécution des tests                             |
| **Statut**                | ✅**RÉSOLU**                                                    |
| **Commit de résolution** | `fd3fdd8` — `test(pdf): tests unitaires pour la génération PDF` |

### Description

La fonction helper `creer_bus()` dans `apps/reservations/tests.py` utilisait des champs `marque` et `modele` qui n'existent **pas** dans le modèle `Bus`.

### Reproduction

```python
# CODE ERRONÉ (avant correction)
def creer_bus(immatriculation='DK-1234-AB', places=30):
    return Bus.objects.create(
        immatriculation=immatriculation,
        nombre_places=places,
        statut='ACTIF',
        marque='Mercedes',    # ❌ Champ inexistant
        modele='Citaro 500',  # ❌ Champ inexistant
    )
```

### Message d'erreur

```
TypeError: Bus() got unexpected keyword arguments: 'marque', 'modele'
```

### Cause racine

Le modèle `Bus` (défini dans `apps/bus/models.py`) ne possède que les champs :
`immatriculation`, `nombre_places`, `statut`, `date_creation`, `date_modification`, `notes`

Il n'y a **jamais eu** de champs `marque` ou `modele`.

### Correction appliquée

```python
# CODE CORRIGÉ
def creer_bus(immatriculation='DK-1234-AB', places=30):
    return Bus.objects.create(
        immatriculation=immatriculation,
        nombre_places=places,
        statut='ACTIF',
    )
```

### Impact de la correction

- ✅ Tous les 31 tests `apps.reservations` passent désormais
- ✅ Aucun autre code affecté

---

## BUG-002 — ✅ RÉSOLU : Couleur invalide dans le générateur PDF

| Champ                           | Valeur                                                                   |
| ------------------------------- | ------------------------------------------------------------------------ |
| **ID**                    | BUG-002                                                                  |
| **Titre**                 | `ValueError: Invalid color value '#x198754'` dans ReportLab            |
| **Sévérité**           | 🔴 Critique                                                              |
| **Fichier**               | `apps/reservations/pdf_generator.py` — méthode `_entete()`         |
| **Sprint détecté**      | Sprint 1 — lors des premiers tests de génération PDF                  |
| **Statut**                | ✅**RÉSOLU**                                                      |
| **Commit de résolution** | `48eb64a` — `feat(pdf): génération de billets PDF avec ReportLab` |

### Description

La méthode `_entete()` du générateur PDF tentait de construire une couleur HTML inline à partir de `colors.HexColor().hexval()`. Cette méthode retourne une chaîne au format `0x198754` (avec préfixe `0x`), ce qui donne `x198754` après `[1:]` — invalide comme couleur HTML.

### Reproduction

```python
from reportlab.lib import colors
c = colors.HexColor('#198754')
print(repr(c.hexval()))   # Affiche : '0x198754'
print(c.hexval()[1:])     # Affiche : 'x198754'  ← INVALIDE
```

### Message d'erreur

```
ValueError: paragraph text
"<para><font color='#x198754' size='14'><b>BILLET DE VOYAGE</b></font></para>"
caused exception Invalid color value '#x198754'
```

### Code erroné

```python
# AVANT (cassé)
Paragraph(
    f"<font color='#{COULEUR_SECONDAIRE.hexval()[1:]}' size='14'>"
    f"<b>BILLET DE VOYAGE</b></font>",
    ParagraphStyle('Billet', alignment=TA_CENTER, fontSize=14, spaceAfter=4)
),
```

### Correction appliquée

```python
# APRÈS (corrigé) — utiliser textColor sur ParagraphStyle au lieu de <font>
Paragraph(
    "<b>BILLET DE VOYAGE</b>",
    ParagraphStyle(
        'Billet',
        alignment=TA_CENTER,
        fontSize=14,
        spaceAfter=4,
        textColor=COULEUR_SECONDAIRE,   # ← Couleur directement dans le style
    )
),
```

### Impact de la correction

- ✅ Génération PDF fonctionnelle — PDF commence par `%PDF`
- ✅ Couleur verte Bootstrap (`#198754`) correctement appliquée
- ✅ `test_generation_pdf_bytes` passe (vérifie `pdf_bytes.startswith(b'%PDF')`)

---

## BUG-003 — 🟠 OUVERTE : `Trajet.__str__()` plante sur `heure_depart` str

| Champ                      | Valeur                                                                                 |
| -------------------------- | -------------------------------------------------------------------------------------- |
| **ID**               | BUG-003                                                                                |
| **Titre**            | `AttributeError: 'str' object has no attribute 'strftime'` dans `Trajet.__str__()` |
| **Sévérité**      | 🟠 Majeure                                                                             |
| **Fichier**          | `apps/trajets/models.py` — ligne 98, méthode `__str__()`                         |
| **Sprint détecté** | Sprint 4 — lors de l'exécution des tests trajets                                     |
| **Statut**           | 🟠**OUVERTE** — Non résolu                                                     |

### Description

La méthode `__str__()` du modèle `Trajet` appelle `.strftime()` sur `heure_depart`. Dans certains contextes (tests, fixtures JSON), `heure_depart` peut être une chaîne `str` au lieu d'un objet `datetime.time`, provoquant une `AttributeError`.

### Message d'erreur

```
AttributeError: 'str' object has no attribute 'strftime'
  File "apps/trajets/models.py", line 98, in __str__
    f"{self.heure_depart.strftime('%Hh%M')}"
```

### Code problématique

```python
# apps/trajets/models.py — ligne ~96
def __str__(self):
    return (
        f"{self.ville_depart} → {self.ville_arrivee} | "
        f"{self.date_depart.strftime('%d/%m/%Y')} à "
        f"{self.heure_depart.strftime('%Hh%M')}"   # ← BUG ici
    )
```

### Impact

- 🟠 `python manage.py test apps.trajets` → 1 ERROR
- ✅ Les 31 tests `apps.reservations` **ne sont PAS affectés**
- 🟡 Interface admin peut planter si heure_depart est str

### Correction proposée

```python
def __str__(self):
    from datetime import time
    heure = self.heure_depart
    if isinstance(heure, str):
        heure = time.fromisoformat(heure)
    return (
        f"{self.ville_depart} → {self.ville_arrivee} | "
        f"{self.date_depart.strftime('%d/%m/%Y')} à "
        f"{heure.strftime('%Hh%M')}"
    )
```

---

## BUG-004 — 🟡 OUVERTE : Cache non invalidé après nouvelle réservation

| Champ                      | Valeur                                                              |
| -------------------------- | ------------------------------------------------------------------- |
| **ID**               | BUG-004                                                             |
| **Titre**            | Cache `api_trajets_disponibles` non invalidé après réservation |
| **Sévérité**      | 🟡 Mineure                                                          |
| **Fichiers**         | `apps/trajets/views.py`, `apps/reservations/views.py`           |
| **Sprint détecté** | Sprint 4 — revue de code                                           |
| **Statut**           | 🟡**OUVERTE** — Non résolu                                  |

### Description

Lorsqu'une réservation est créée (POST `/reservations/creer/<trajet_id>/`), le nombre de places disponibles change sur le trajet. Cependant, le cache `api_trajets_disponibles` (TTL: 5 minutes) n'est pas invalidé. L'API `/api/trajets/disponibles/` peut donc retourner des données périmées pendant 5 minutes.

### Scénario de reproduction

```
1. GET /api/trajets/disponibles/  → Trajet A : 5 places disponibles (mis en cache)
2. POST /reservations/creer/1/   → Alice réserve 5 places sur Trajet A
3. GET /api/trajets/disponibles/  → Toujours "5 places" (cache périmé) ← BUG
4. (5 min plus tard) GET /api/trajets/disponibles/ → 0 places (cache expiré, OK)
```

### Correction proposée

```python
# Dans ReservationCreerView.post(), après reservation.save() :
from django.core.cache import cache
cache.delete('api_trajets_disponibles')  # Invalider le cache

# Alternative : cache avec clé spécifique par trajet
cache_key = f'trajet_disponible_{trajet.pk}'
cache.delete(cache_key)
```

---

## BUG-005 — 🟡 OUVERTE : Export CSV sans pagination (gros volumes)

| Champ                      | Valeur                                                  |
| -------------------------- | ------------------------------------------------------- |
| **ID**               | BUG-005                                                 |
| **Titre**            | Export CSV charge toutes les réservations en mémoire  |
| **Sévérité**      | 🟡 Mineure                                              |
| **Fichier**          | `apps/reservations/views.py` — `export_csv_view()` |
| **Sprint détecté** | Sprint 2 — revue de code                               |
| **Statut**           | 🟡**OUVERTE** — Non résolu                      |

### Description

La vue `export_csv_view()` charge **toutes** les réservations du client en mémoire avant d'écrire le CSV. Pour un client avec des milliers de réservations, cela peut provoquer une forte consommation mémoire.

### Code actuel

```python
reservations = Reservation.objects.filter(client=user).select_related(...)
# Toutes les réservations chargées en mémoire
for r in reservations:
    writer.writerow([...])
```

### Correction proposée

```python
# Utiliser iterator() pour traitement en streaming
for r in reservations.iterator(chunk_size=200):
    writer.writerow([...])
```

---

## BUG-006 — 🟢 TRIVIALE : Session "expire" masquée par SESSION_SAVE_EVERY_REQUEST

| Champ                      | Valeur                                                     |
| -------------------------- | ---------------------------------------------------------- |
| **ID**               | BUG-006                                                    |
| **Titre**            | `SESSION_COOKIE_AGE=86400` mais reset à chaque requête |
| **Sévérité**      | 🟢 Triviale                                                |
| **Fichier**          | `transport_project/settings.py`                          |
| **Sprint détecté** | Sprint 1 — revue de code                                  |
| **Statut**           | 🟢**OUVERTE** — Non bloquant                        |

### Description

Le paramètre `SESSION_SAVE_EVERY_REQUEST = True` renouvelle la session à chaque requête. Ainsi, la session de 24h (`SESSION_COOKIE_AGE = 86400`) ne expire en pratique **jamais** tant que l'utilisateur navigue sur le site. Un utilisateur peut rester indéfiniment connecté.

### Impact

- Comportement acceptable pour une app de transport (UX améliorée)
- Légère sur-consommation de la base de sessions
- Pas un risque sécurité critique

### Correction optionnelle

```python
SESSION_SAVE_EVERY_REQUEST = False  # Expiration réelle à 24h d'inactivité
```

---

## 📋 Suivi des anomalies

```
Semaine 1 (Sprint 1) :
  ├─ BUG-002 détecté → résolu le jour même (commit 48eb64a)
  └─ BUG-006 identifié → accepté (non bloquant)

Semaine 2 (Sprint 2) :
  └─ BUG-005 identifié → reporté (non bloquant)

Semaine 3 (Sprint 3) :
  └─ BUG-004 identifié → reporté (à corriger v2.1)

Semaine 4 (Sprint 4) :
  ├─ BUG-001 détecté → résolu le jour même (commit fd3fdd8)
  └─ BUG-003 détecté → en attente correction
```

---

## 🔧 Recommandations pour v2.1

1. **BUG-003** (Priorité 1) — Corriger `Trajet.__str__()` pour gérer `str` vs `time`
2. **BUG-004** (Priorité 2) — Invalider le cache après chaque réservation/annulation
3. **BUG-005** (Priorité 3) — Ajouter `iterator()` dans l'export CSV
4. **BUG-006** (Optionnel) — Revoir la politique de session
