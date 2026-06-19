# 📖 Guide Utilisateur — Transport Réservation v2.0

> **Application de réservation de billets de bus**  
> **Audience :** Utilisateurs finaux (voyageurs)  
> **Version :** 2.0.0 — Novembre 2024  

---

## 📑 Table des matières

1. [Introduction](#1-introduction)
2. [Créer un compte](#2-créer-un-compte)
3. [Se connecter](#3-se-connecter)
4. [Rechercher un trajet](#4-rechercher-un-trajet)
5. [Effectuer une réservation](#5-effectuer-une-réservation)
6. [Télécharger son billet PDF](#6-télécharger-son-billet-pdf)
7. [Consulter le dashboard](#7-consulter-le-dashboard)
8. [Annuler une réservation](#8-annuler-une-réservation)
9. [Règles de remboursement](#9-règles-de-remboursement)
10. [Exporter ses réservations CSV](#10-exporter-ses-réservations-csv)
11. [Consulter les statistiques](#11-consulter-les-statistiques)
12. [Gérer son profil](#12-gérer-son-profil)
13. [FAQ](#13-faq)

---

## 1. Introduction

**Transport Réservation** est une plateforme en ligne permettant de réserver des billets de bus en toute simplicité. Vous pouvez rechercher des trajets, réserver vos places, recevoir votre billet par email et l'annuler si nécessaire.

### Ce que vous pouvez faire avec cette application :

| ✅ Fonctionnalité | Description |
|------------------|-------------|
| 🔍 Recherche | Chercher un trajet par ville, date, prix ou horaire |
| 🎫 Réservation | Réserver jusqu'à 10 places sur un trajet |
| 📄 Billet PDF | Télécharger/recevoir votre billet avec QR code |
| 📧 Email | Confirmation automatique par email |
| ❌ Annulation | Annuler avec remboursement selon délai |
| 📊 Statistiques | Voir vos dépenses et historique |
| 📤 Export CSV | Exporter toutes vos réservations |

### Accès à l'application

```
URL Principale :  http://votre-domaine.com/
Connexion :       http://votre-domaine.com/accounts/connexion/
Inscription :     http://votre-domaine.com/accounts/inscription/
```

---

## 2. Créer un compte

### 2.1 Accéder au formulaire d'inscription

Rendez-vous sur la page d'accueil et cliquez sur le bouton **"S'inscrire"** dans la barre de navigation, ou accédez directement à :

```
http://votre-domaine.com/accounts/inscription/
```

### 2.2 Remplir le formulaire d'inscription

| Champ | Type | Obligatoire | Contraintes |
|-------|------|:-----------:|-------------|
| **Prénom** | Texte | ✅ | 2–50 caractères |
| **Nom** | Texte | ✅ | 2–50 caractères |
| **Email** | Email | ✅ | Format valide, unique |
| **Téléphone** | Texte | ✅ | Format : `+221 XX XXX XX XX` |
| **Mot de passe** | Mot de passe | ✅ | Min. 8 caractères |
| **Confirmer le mot de passe** | Mot de passe | ✅ | Doit correspondre |

### 2.3 Validation et connexion automatique

Après validation du formulaire :
- ✅ Votre compte est créé immédiatement
- ✅ Vous êtes **connecté automatiquement**
- ✅ Vous êtes redirigé vers votre **dashboard personnel**
- ✅ Un message de bienvenue s'affiche : *"Bienvenue [Prénom] ! Votre compte a été créé avec succès."*

> ⚠️ **Important :** Votre adresse email est votre identifiant de connexion. Choisissez une adresse valide car vous recevrez vos billets à cette adresse.

---

## 3. Se connecter

### 3.1 Accéder à la page de connexion

```
http://votre-domaine.com/accounts/connexion/
```

Ou cliquez sur **"Se connecter"** dans la barre de navigation.

### 3.2 Formulaire de connexion

| Champ | Description |
|-------|-------------|
| **Email** | Votre adresse email (identifiant) |
| **Mot de passe** | Votre mot de passe |

### 3.3 Après connexion

Vous êtes redirigé vers votre **dashboard personnel** (`/reservations/dashboard/`).

> 💡 **Astuce :** Si vous avez déjà une session active, la page de connexion vous redirige automatiquement vers votre dashboard.

### 3.4 Se déconnecter

Pour vous déconnecter en toute sécurité :
1. Cliquez sur votre **prénom** en haut à droite
2. Sélectionnez **"Se déconnecter"**
3. Vous êtes redirigé vers la page d'accueil

```
URL de déconnexion : /accounts/deconnexion/
```

---

## 4. Rechercher un trajet

### 4.1 Accéder à la liste des trajets

```
http://votre-domaine.com/trajets/
```

La liste affiche uniquement les trajets **à venir** (date de départ ≥ aujourd'hui) avec des places disponibles.

### 4.2 Filtres de recherche de base

Utilisez le formulaire de recherche en haut de la liste :

| Filtre | Description | Exemple |
|--------|-------------|---------|
| **Ville de départ** | Nom de la ville de départ | `Dakar` |
| **Ville d'arrivée** | Nom de la ville d'arrivée | `Thiès` |
| **Date de départ** | Date souhaitée | `2024-12-01` |

### 4.3 Filtres avancés (Sprint 3)

Développez les **"Filtres avancés"** pour affiner votre recherche :

| Filtre | Description | Valeurs possibles |
|--------|-------------|-------------------|
| **Prix minimum** | Budget minimum | Ex : `500` (FCFA) |
| **Prix maximum** | Budget maximum | Ex : `5000` (FCFA) |
| **Créneau horaire** | Plage horaire du départ | `matin`, `après-midi`, `soir`, `nuit` |
| **Places minimales** | Nombre de places requises | `1` à `10` |
| **Exclure complets** | Masquer les trajets sans places | ✅ / ☐ |

#### Définition des créneaux horaires

| Créneau | Plage horaire |
|---------|:-------------:|
| 🌅 Matin | 06h00 → 11h59 |
| ☀️ Après-midi | 12h00 → 17h59 |
| 🌆 Soir | 18h00 → 23h59 |
| 🌙 Nuit | 00h00 → 05h59 |

### 4.4 Exemple d'URL de recherche filtrée

```
/trajets/?ville_depart=Dakar&ville_arrivee=Thies&prix_max=3000&creneau=matin&places_min=2
```

### 4.5 Informations affichées par trajet

Chaque trajet dans la liste affiche :

```
┌─────────────────────────────────────────────────────────────────┐
│  🚌 Dakar → Thiès                                               │
│  📅 01/12/2024  ⏰ 08h30   💰 2 500 FCFA/place                  │
│  🪑 15 places disponibles   Bus AB-1234-CD                      │
│  [  Voir détails  ]  [  Réserver maintenant  ]                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Effectuer une réservation

> ⚠️ **Connexion requise.** Vous devez être connecté pour réserver. Si vous ne l'êtes pas, vous serez automatiquement redirigé vers la page de connexion.

### 5.1 Accéder au formulaire de réservation

Depuis la liste des trajets ou la page de détail d'un trajet, cliquez sur **"Réserver maintenant"**.

```
URL : /reservations/creer/?trajet_id={ID_DU_TRAJET}
```

### 5.2 Remplir le formulaire

| Champ | Description | Contraintes |
|-------|-------------|-------------|
| **Trajet** | Sélectionné automatiquement | Non modifiable |
| **Nombre de places** | Nombre de places à réserver | 1 à 10 maximum |
| **Notes** | Remarques optionnelles | Texte libre |

> ⚠️ **Limite :** Vous ne pouvez pas réserver plus de **10 places** par réservation.  
> ⚠️ **Disponibilité :** Le nombre de places demandé doit être disponible sur le trajet.

### 5.3 Ce qui se passe après validation

Après avoir cliqué sur **"Confirmer la réservation"** :

```
Étape 1 ──► Validation de la disponibilité des places
Étape 2 ──► Enregistrement de la réservation (statut : EN_ATTENTE)
Étape 3 ──► Génération automatique du billet PDF avec QR code
Étape 4 ──► Envoi automatique du billet par email
Étape 5 ──► Notification système : "Réservation confirmée !"
Étape 6 ──► Redirection vers le dashboard
```

### 5.4 Confirmation

Un message vert s'affiche en haut de la page :

```
✅ Votre réservation a été créée avec succès ! 
   Votre billet a été envoyé à votre adresse email.
```

---

## 6. Télécharger son billet PDF

### 6.1 Depuis le dashboard

Dans votre dashboard, chaque réservation possède un bouton **"📥 Télécharger le billet"**.

### 6.2 URL directe

```
/reservations/{ID_RESERVATION}/billet/
```

> 🔒 **Sécurité :** Vous ne pouvez télécharger que VOS propres billets. Toute tentative d'accès à un billet d'un autre utilisateur retourne une erreur 403.

### 6.3 Contenu du billet PDF

Le billet PDF généré contient :

```
┌───────────────────────────────────────────────────────────┐
│          🚌 TRANSPORT RÉSERVATION                          │
│              BILLET DE VOYAGE                             │
│                                                           │
│  Référence : RES-2024-001234                              │
│  Client : Jean DUPONT                                     │
│  Email : jean.dupont@email.com                            │
│  Téléphone : +221 77 123 45 67                            │
│                                                           │
│  ──────────────────────────────                           │
│  DÉTAILS DU TRAJET                                        │
│  ──────────────────────────────                           │
│  Départ : Dakar                    [QR CODE]              │
│  Arrivée : Thiès                                          │
│  Date : 01/12/2024                                        │
│  Heure : 08h30                                            │
│  Bus : AB-1234-CD                                         │
│                                                           │
│  Nombre de places : 2                                     │
│  Prix total : 5 000 FCFA                                  │
│                                                           │
│  Statut : ✅ CONFIRMÉE                                    │
└───────────────────────────────────────────────────────────┘
```

### 6.4 QR Code

Le QR code encode la référence unique de votre réservation et peut être scanné à bord du bus pour validation.

---

## 7. Consulter le dashboard

Le dashboard est votre espace personnel. Accessible via :

```
/reservations/dashboard/
```

Ou en cliquant sur **"Mon espace"** dans la navigation.

### 7.1 Récapitulatif en chiffres

En haut du dashboard, 4 statistiques instantanées :

| Indicateur | Description |
|-----------|-------------|
| 📋 Total réservations | Nombre total de réservations créées |
| ✅ Actives | Réservations en attente ou confirmées |
| ❌ Annulées | Réservations annulées |
| 💰 Total dépensé | Montant total de vos réservations actives |

### 7.2 Liste des réservations

Tableau paginé (10 par page) avec pour chaque réservation :

| Colonne | Description |
|---------|-------------|
| **Référence** | Identifiant unique (ex: `RES-2024-001`) |
| **Trajet** | Ville départ → Ville arrivée |
| **Date départ** | Date et heure du départ |
| **Places** | Nombre de places réservées |
| **Prix total** | Montant payé |
| **Statut** | Badge coloré : EN_ATTENTE / CONFIRMÉE / ANNULÉE |
| **Actions** | Boutons : Détails, Billet, Annuler |

### 7.3 Statuts des réservations

| Statut | Couleur | Description |
|--------|:-------:|-------------|
| `EN_ATTENTE` | 🟡 Jaune | Réservation créée, en attente de traitement |
| `CONFIRMÉE` | 🟢 Vert | Réservation validée |
| `ANNULÉE` | 🔴 Rouge | Réservation annulée (avec ou sans remboursement) |

---

## 8. Annuler une réservation

### 8.1 Conditions d'annulation

Une réservation peut être annulée si :
- ✅ Elle n'est **pas déjà annulée**
- ✅ Le départ n'a **pas encore eu lieu**

### 8.2 Procédure d'annulation

1. Allez sur votre **dashboard** (`/reservations/dashboard/`)
2. Trouvez la réservation à annuler
3. Cliquez sur le bouton **"❌ Annuler"**
4. Lisez le **message d'information** sur le remboursement estimé
5. Saisissez optionnellement une **raison d'annulation**
6. Cliquez sur **"Confirmer l'annulation"**

### 8.3 Message de confirmation

```
URL : /reservations/{ID}/annuler/

📋 FORMULAIRE D'ANNULATION
───────────────────────────────────
Trajet : Dakar → Thiès
Date de départ : 01/12/2024 à 08h30
Places réservées : 2
Prix payé : 5 000 FCFA

⚠️ Remboursement estimé : 5 000 FCFA (100%)
   (Annulation à plus de 24h du départ)

Raison (optionnel) : [________________________]

[ Annuler la réservation ] [ Retour ]
```

### 8.4 Après annulation

- 📧 Un email de confirmation d'annulation est envoyé automatiquement
- 📊 Le statut de la réservation passe à `ANNULÉE`
- 💰 Le montant de remboursement est affiché (simulation)
- 📝 Un log est enregistré dans `reservations.log`

---

## 9. Règles de remboursement

Le système applique automatiquement des règles de remboursement selon le délai d'annulation :

### 9.1 Tableau des taux de remboursement

| Délai avant le départ | Taux de remboursement | Exemple (sur 5 000 FCFA) |
|----------------------|:---------------------:|:------------------------:|
| **Plus de 24 heures** | **100%** ✅ | 5 000 FCFA remboursés |
| **Entre 2 et 24 heures** | **50%** ⚠️ | 2 500 FCFA remboursés |
| **Moins de 2 heures** | **0%** ❌ | 0 FCFA remboursé |

### 9.2 Exemples concrets

```
Scénario 1 : Départ le 01/12 à 08h30
   Annulation le 29/11 à 10h00 (> 24h) → Remboursement : 100% ✅
   
Scénario 2 : Départ le 01/12 à 08h30
   Annulation le 01/12 à 06h00 (entre 2h et 24h) → Remboursement : 50% ⚠️
   
Scénario 3 : Départ le 01/12 à 08h30
   Annulation le 01/12 à 07h00 (< 2h) → Remboursement : 0% ❌
```

> ℹ️ **Note :** Le remboursement affiché est **simulé**. Le traitement réel du remboursement s'effectue selon les procédures de votre opérateur.

---

## 10. Exporter ses réservations CSV

### 10.1 Télécharger l'export

Depuis votre dashboard, cliquez sur **"📤 Exporter en CSV"** ou accédez directement à :

```
/reservations/export/csv/
```

### 10.2 Format du fichier CSV

Le fichier téléchargé est nommé automatiquement :

```
reservations_votre.email@exemple.com_2024-12-01.csv
```

### 10.3 Structure du CSV (12 colonnes)

| N° | Colonne | Description | Exemple |
|:--:|---------|-------------|---------|
| 1 | `Référence` | ID unique de la réservation | `1` |
| 2 | `Trajet` | Départ → Arrivée | `Dakar → Thiès` |
| 3 | `Date réservation` | Date de création | `2024-11-28` |
| 4 | `Date départ` | Date du trajet | `2024-12-01` |
| 5 | `Heure départ` | Heure du trajet | `08:30` |
| 6 | `Ville départ` | Ville de départ | `Dakar` |
| 7 | `Ville arrivée` | Ville d'arrivée | `Thiès` |
| 8 | `Places` | Nombre de places | `2` |
| 9 | `Prix unitaire` | Prix par place | `2500.00` |
| 10 | `Prix total` | Montant total | `5000.00` |
| 11 | `Statut` | Statut de la réservation | `CONFIRMEE` |
| 12 | `Raison annulation` | Si annulée, la raison | `Voyage annulé` |

### 10.4 Compatibilité

- **Encodage :** UTF-8 BOM (compatible Excel, LibreOffice, Google Sheets)
- **Séparateur :** Virgule (`,`)
- **Ouverture :** Double-clic sur le fichier dans Excel ou LibreOffice Calc

---

## 11. Consulter les statistiques

### 11.1 Accéder aux statistiques

```
/reservations/stats/
```

Ou depuis votre dashboard, cliquez sur **"📊 Mes statistiques"**.

### 11.2 Graphiques disponibles

#### Dépenses par mois (Graphique en barres)

```
FCFA
 ┤
6000 ┤        ████
5000 ┤  ████  ████  ████
4000 ┤  ████  ████  ████  ████
3000 ┤  ████  ████  ████  ████
2000 ┤  ████  ████  ████  ████
1000 ┤  ████  ████  ████  ████
     └──────────────────────────
     Oct   Nov   Déc   Jan
```

#### Trajets populaires (Graphique en camembert)

Répartition de vos trajets par destination.

### 11.3 Données affichées

| Indicateur | Description |
|-----------|-------------|
| Total dépensé | Somme de toutes vos réservations actives |
| Trajet favori | La destination que vous prenez le plus souvent |
| Mois le plus actif | Le mois avec le plus de réservations |

---

## 12. Gérer son profil

### 12.1 Accéder au profil

```
/accounts/profil/
```

Ou cliquez sur votre nom en haut à droite → **"Mon profil"**.

### 12.2 Informations modifiables

| Champ | Description |
|-------|-------------|
| **Prénom** | Votre prénom |
| **Nom** | Votre nom de famille |
| **Téléphone** | Votre numéro de téléphone |

> ⚠️ **Note :** L'adresse email n'est **pas modifiable** via le profil car elle est votre identifiant de connexion. Contactez l'administrateur pour tout changement d'email.

---

## 13. FAQ

### ❓ Je n'ai pas reçu mon billet par email

1. Vérifiez votre dossier **Spams/Courriers indésirables**
2. Attendez quelques minutes (traitement asynchrone possible)
3. Téléchargez directement le billet depuis votre dashboard
4. Contactez le support si le problème persiste

### ❓ Je n'arrive pas à me connecter

- Vérifiez que vous utilisez bien votre **adresse email** (pas votre nom d'utilisateur)
- Vérifiez que la touche Majuscules n'est pas activée
- Utilisez la fonction "Mot de passe oublié" si disponible

### ❓ Le trajet que je veux n'apparaît pas

- Le trajet est peut-être **complet** (0 places disponibles) — activez le filtre "Exclure complets"
- La date de départ est peut-être **passée** — seuls les trajets futurs sont affichés
- Vérifiez l'orthographe des villes dans votre recherche

### ❓ Je ne peux pas annuler ma réservation

Vérifiez que :
- La réservation n'est pas **déjà annulée**
- Le **départ n'est pas passé**
- Vous êtes bien l'**auteur** de la réservation

### ❓ Mon remboursement est de 0% — pourquoi ?

Si vous annulez **moins de 2 heures** avant le départ, le système applique un taux de 0% conformément à la politique tarifaire. Planifiez vos annulations à l'avance !

### ❓ Combien de places puis-je réserver maximum ?

Vous pouvez réserver jusqu'à **10 places** par réservation. Pour plus de places, créez plusieurs réservations.

### ❓ Comment lire le QR code sur mon billet ?

Le QR code peut être scanné avec n'importe quelle application de lecture QR code sur votre smartphone (appareil photo iOS/Android, Google Lens, etc.) ou présenté au personnel lors de l'embarquement.

---

## 📞 Support

| Canal | Contact |
|-------|---------|
| 📧 Email | support@transport-reservation.com |
| 🌐 Site web | http://votre-domaine.com/ |
| 🕐 Horaires | Lun–Ven, 8h00–18h00 |

---

<div align="center">

*[← README Projet](04_README_PROJET.md) • [Guide Administrateur →](06_GUIDE_ADMINISTRATEUR.md)*

</div>
