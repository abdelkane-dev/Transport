# 🤝 Guide de Contribution — Transport Réservation

> **Version :** 2.0.0  
> **Dernière mise à jour :** Novembre 2024  
> **Audience :** Développeurs souhaitant contribuer au projet

---

## 📑 Table des matières

1. [Code de conduite](#1-code-de-conduite)
2. [Comment contribuer](#2-comment-contribuer)
3. [Environnement de développement](#3-environnement-de-développement)
4. [Conventions Git](#4-conventions-git)
5. [Conventions de code](#5-conventions-de-code)
6. [Processus de review](#6-processus-de-review)
7. [Templates Issues GitHub](#7-templates-issues-github)
8. [Template Pull Request](#8-template-pull-request)
9. [Tests obligatoires](#9-tests-obligatoires)
10. [Checklist avant soumission](#10-checklist-avant-soumission)

---

## 1. Code de conduite

### Nos engagements

En tant que membres et contributeurs, nous nous engageons à rendre la participation à notre projet une expérience sans harcèlement pour tout le monde, indépendamment de l'âge, la taille corporelle, le handicap, l'ethnicité, l'identité de genre, le niveau d'expérience, la nationalité, l'apparence personnelle, la race, la religion ou l'identité et l'orientation sexuelles.

### Standards attendus

✅ **Comportements positifs :**
- Utiliser un langage accueillant et inclusif
- Respecter les points de vue et expériences divergents
- Accepter gracieusement les critiques constructives
- Se concentrer sur ce qui est le mieux pour la communauté

❌ **Comportements inacceptables :**
- Utilisation de langage ou d'images sexualisés
- Trolling, commentaires insultants/désobligeants
- Harcèlement public ou privé
- Publication d'informations privées d'autrui

---

## 2. Comment contribuer

### 2.1 Signaler un bug

1. Vérifiez que le bug n'est pas **déjà signalé** dans les [Issues](https://github.com/votre-org/transport-reservation/issues)
2. Créez une nouvelle issue en utilisant le **[template Bug Report](#bug-report)**
3. Fournissez **autant de détails que possible** :
   - Version du projet, Python, Django
   - Étapes de reproduction
   - Comportement attendu vs observé
   - Logs d'erreur

### 2.2 Proposer une fonctionnalité

1. Ouvrez une issue avec le **[template Feature Request](#feature-request)**
2. Décrivez clairement le **besoin utilisateur**
3. Proposez une **solution technique** si possible
4. Attendez la validation d'un mainteneur avant de commencer le développement

### 2.3 Soumettre du code (Pull Request)

```
1. Fork le dépôt → 2. Créer une branche → 3. Développer → 4. Tester → 5. PR
```

**Étapes détaillées :**

```bash
# 1. Fork et clone
git clone https://github.com/votre-username/transport-reservation.git
cd transport-reservation

# 2. Créer votre branche de fonctionnalité
git checkout -b feat/nom-de-la-feature
# ou
git checkout -b fix/nom-du-bug

# 3. Développer et committer
git add .
git commit -m "feat(module): description courte de la feature"

# 4. Pousser et créer la PR
git push origin feat/nom-de-la-feature
# → Créer la PR sur GitHub
```

---

## 3. Environnement de développement

### 3.1 Setup complet

```bash
# Clone le dépôt
git clone https://github.com/votre-org/transport-reservation.git
cd transport-reservation

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs locales

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur de test
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### 3.2 Structure des branches

| Branche | Description | Protection |
|---------|-------------|:----------:|
| `main` | Production stable | 🔒 Protégée |
| `develop` | Intégration des features | 🔒 Protégée |
| `feat/*` | Nouvelles fonctionnalités | ❌ |
| `fix/*` | Corrections de bugs | ❌ |
| `docs/*` | Documentation uniquement | ❌ |
| `test/*` | Tests uniquement | ❌ |
| `refactor/*` | Refactoring | ❌ |
| `chore/*` | Maintenance | ❌ |

### 3.3 Flux de travail recommandé

```
feat/ma-feature
       │
       ▼
   develop  ←─── PR Review ────── feat/autre-feature
       │
       ▼
     main (release)
```

---

## 4. Conventions Git

### 4.1 Conventional Commits

Le projet utilise le format **Conventional Commits** :

```
<type>(<scope>): <description courte>

[corps optionnel]

[pied de page optionnel]
```

**Types autorisés :**

| Type | Emoji | Usage |
|------|:-----:|-------|
| `feat` | ✨ | Nouvelle fonctionnalité |
| `fix` | 🐛 | Correction de bug |
| `docs` | 📚 | Documentation uniquement |
| `chore` | 🔧 | Maintenance, build, dépendances |
| `refactor` | ♻️ | Refactoring (sans nouvelle feature ni fix) |
| `test` | ✅ | Ajout ou modification de tests |
| `perf` | ⚡ | Amélioration des performances |
| `style` | 💄 | Formatage (pas de changement logique) |
| `ci` | 🔄 | Intégration continue |

**Scopes du projet :**

| Scope | Description |
|-------|-------------|
| `accounts` | Application comptes utilisateurs |
| `bus` | Application gestion des bus |
| `trajets` | Application trajets |
| `reservation` | Application réservations |
| `api` | API REST |
| `pdf` | Génération PDF |
| `email` | Service email |
| `cache` | Système de cache |
| `logging` | Système de logs |
| `security` | Sécurité |
| `settings` | Configuration Django |
| `deps` | Dépendances |
| `init` | Initialisation |
| `sprint` | Journal de sprint |

### 4.2 Exemples de messages de commit

```bash
# ✅ Bon
git commit -m "feat(reservation): ajouter le remboursement automatique lors de l'annulation"
git commit -m "fix(pdf): corriger la couleur invalide HexColor dans ParagraphStyle"
git commit -m "docs(api): documenter l'endpoint /api/trajets/disponibles/"
git commit -m "test(reservation): ajouter tests pour la règle de remboursement"
git commit -m "chore(deps): mettre à jour reportlab de 4.1 à 4.2.2"
git commit -m "refactor(views): extraire la logique PDF dans BilletPDFGenerator"

# ❌ Mauvais
git commit -m "fix bug"
git commit -m "modifications"
git commit -m "WIP"
git commit -m "asdfgh"
```

### 4.3 Nommage des branches

```bash
# ✅ Bon
feat/generation-billet-pdf
fix/bug-003-trajet-str-heure-depart
docs/api-documentation-complete
test/tests-remboursement-annulation
refactor/extraction-service-email

# ❌ Mauvais
ma-branche
fix-truc
feature1
FEATURE
```

### 4.4 Tags de version

```bash
# Format : vMAJOR.MINOR.PATCH
git tag -a v2.0.0 -m "Release v2.0.0 — 12 features, 4 sprints"
git tag -a v2.1.0 -m "Ajout de l'authentification OAuth"
git tag -a v2.1.1 -m "Fix BUG-003 Trajet.__str__() AttributeError"
```

---

## 5. Conventions de code

### 5.1 Style Python

Le projet suit **PEP 8** avec quelques conventions spécifiques :

```python
# ✅ Bon : Docstrings pour toutes les classes et méthodes publiques
class ReservationCreerView(LoginRequiredMixin, CreateView):
    """
    Vue de création d'une réservation.
    POST /reservations/creer/
    Accessible uniquement aux utilisateurs connectés.
    """
    
    def post(self, request, *args, **kwargs):
        """Crée la réservation et génère le billet PDF."""
        ...

# ✅ Bon : Commentaires avec contexte sprint
# SPRINT 1 – Feature 1 : Intégration du générateur de billets PDF
from .pdf_generator import BilletPDFGenerator

# ✅ Bon : Loggers nommés
logger = logging.getLogger('transport.reservations')

# ✅ Bon : Type hints pour les méthodes complexes
def peut_etre_annulee_avec_remboursement(self) -> tuple[bool, float, str]:
    ...
```

### 5.2 Règles spécifiques au projet

| Règle | Description |
|-------|-------------|
| **Pas de marque/modèle sur Bus** | Le modèle Bus n'a PAS de champs `marque` ou `modele` |
| **textColor en ParagraphStyle** | Utiliser `textColor=COULEUR_X` dans `ParagraphStyle`, jamais `<font color>` inline |
| **Isolation client** | Toujours filtrer `filter(client=request.user)` dans les vues client |
| **full_clean() avant save** | Appeler `full_clean()` dans `clean()` avant toute sauvegarde |
| **Logging obligatoire** | Logger toutes les actions de réservation/annulation |
| **MaxValueValidator(10)** | La limite de 10 places par réservation est une règle métier |

### 5.3 Structure des vues

```python
# Pattern CBV recommandé
class MaView(LoginRequiredMixin, ListView):
    """Docstring claire."""
    
    model = MonModel
    template_name = 'app/template.html'
    context_object_name = 'objets'
    login_url = '/accounts/connexion/'
    
    def get_queryset(self):
        """Surcharger pour filtrer/optimiser les requêtes."""
        return MonModel.objects.select_related('relation').filter(
            user=self.request.user  # Toujours isoler par utilisateur
        )
    
    def get_context_data(self, **kwargs):
        """Ajouter des données supplémentaires au contexte."""
        context = super().get_context_data(**kwargs)
        context['extra_data'] = ...
        return context
```

### 5.4 Tests obligatoires

Chaque nouvelle fonctionnalité **DOIT** avoir des tests correspondants :

```python
class MaFonctionnaliteTests(TestCase):
    """Tests pour MaFonctionnalite."""
    
    def setUp(self):
        """Configuration commune aux tests."""
        self.user = User.objects.create_user(
            email='test@test.com',
            password='password123',
            prenom='Test',
            nom='User'
        )
        self.bus = Bus.objects.create(
            immatriculation='TEST-001',
            nombre_places=30,
            statut='ACTIF'
        )
    
    def test_cas_nominal(self):
        """Test du cas d'utilisation normal."""
        ...
        self.assertEqual(resultat, valeur_attendue)
    
    def test_cas_limite(self):
        """Test des cas limites et edge cases."""
        ...
    
    def test_erreur_validation(self):
        """Test que les erreurs de validation sont correctement levées."""
        with self.assertRaises(ValidationError):
            ...
```

---

## 6. Processus de review

### 6.1 Critères d'acceptation d'une PR

Une Pull Request est acceptée si :

- [ ] ✅ Tous les tests existants passent (`python manage.py test`)
- [ ] ✅ Les nouveaux tests couvrent la fonctionnalité ajoutée
- [ ] ✅ Le code respecte PEP 8 et les conventions du projet
- [ ] ✅ La documentation est mise à jour si nécessaire
- [ ] ✅ Les messages de commit suivent Conventional Commits
- [ ] ✅ La PR cible la branche `develop` (pas `main` directement)
- [ ] ✅ Au moins 1 approbation d'un mainteneur
- [ ] ✅ Pas de conflits avec la branche cible

### 6.2 Processus de review

```
1. Developer ouvre une PR → 2. CI tests auto → 3. Review humaine → 4. Merge
        │                           │                    │
        ▼                           ▼                    ▼
   Remplit template          Pass ✅ ou Fail ❌    Approuve ✅ ou 
   Ajoute reviewers                                 Demande changes 🔄
```

### 6.3 Durée de review estimée

| Type de changement | Délai estimé |
|-------------------|:------------:|
| Documentation | 1 jour |
| Fix mineur (1-10 lignes) | 1-2 jours |
| Nouvelle feature | 2-5 jours |
| Refactoring majeur | 3-7 jours |

---

## 7. Templates Issues GitHub

### Bug Report

```markdown
---
name: 🐛 Bug Report
about: Signaler un problème ou comportement inattendu
labels: bug, needs-triage
---

## 📋 Description du bug

<!-- Description claire et concise du bug -->

## 🔁 Étapes de reproduction

1. Aller sur '...'
2. Cliquer sur '...'
3. Faire défiler jusqu'à '...'
4. Observer l'erreur

## ✅ Comportement attendu

<!-- Décrivez ce qui devrait se passer -->

## ❌ Comportement observé

<!-- Décrivez ce qui se passe réellement -->

## 📸 Captures d'écran

<!-- Si applicable, ajoutez des captures d'écran -->

## 🔍 Logs d'erreur

```
Collez ici les logs d'erreur (transport.log / errors.log)
```

## 🛠️ Environnement

- **OS :** [ex: Windows 11 / Ubuntu 22.04 / macOS 14]
- **Python :** [ex: 3.11.5]
- **Django :** [ex: 5.1.4]
- **Version du projet :** [ex: v2.0.0]
- **Navigateur (si applicable) :** [ex: Chrome 119]

## 📌 Contexte supplémentaire

<!-- Toute autre information utile -->

## ✅ Checklist

- [ ] J'ai vérifié que ce bug n'est pas déjà signalé
- [ ] J'ai fourni les étapes de reproduction
- [ ] J'ai ajouté les logs d'erreur pertinents
```

---

### Feature Request

```markdown
---
name: ✨ Feature Request
about: Proposer une nouvelle fonctionnalité
labels: enhancement, needs-discussion
---

## 🎯 Problème résolu

<!-- Quel problème cette feature résout-elle ? Ex: "Je suis frustré quand..." -->

## 💡 Solution proposée

<!-- Description claire de la fonctionnalité souhaitée -->

## 🔄 Alternatives considérées

<!-- D'autres solutions que vous avez envisagées -->

## 📋 Critères d'acceptation

<!-- Comment saura-t-on que cette feature est "finie" ? -->
- [ ] Critère 1
- [ ] Critère 2
- [ ] Tests ajoutés
- [ ] Documentation mise à jour

## 🏗️ Impact technique estimé

<!-- Quels modules/fichiers seraient affectés ? -->

## 📌 Priorité

- [ ] 🔴 Critique (bloque les utilisateurs)
- [ ] 🟠 Haute (amélioration importante)
- [ ] 🟡 Moyenne (nice-to-have)
- [ ] 🟢 Basse (cosmétique)

## ✅ Checklist

- [ ] J'ai vérifié que cette feature n'est pas déjà demandée
- [ ] J'ai discuté de cette feature en amont (si complexe)
```

---

### Question / Support

```markdown
---
name: ❓ Question / Support
about: Poser une question ou demander de l'aide
labels: question
---

## ❓ Ma question

<!-- Posez votre question ici -->

## 🔍 Ce que j'ai déjà essayé

<!-- Décrivez vos tentatives pour résoudre le problème -->

## 📚 Documentation consultée

<!-- Quelle documentation avez-vous déjà lue ? -->

## 🛠️ Environnement

- **Python :** [ex: 3.11.5]
- **Django :** [ex: 5.1.4]
- **OS :** [ex: Ubuntu 22.04]
```

---

## 8. Template Pull Request

```markdown
## 📋 Description

<!-- Description claire des changements apportés -->

## 🎯 Type de changement

- [ ] 🐛 Fix (correction d'un bug)
- [ ] ✨ Feature (nouvelle fonctionnalité)
- [ ] 📚 Documentation
- [ ] ♻️ Refactoring
- [ ] 🔧 Chore (maintenance)
- [ ] ✅ Tests
- [ ] ⚡ Performance

## 🔗 Issues liées

<!-- Ferme #XXX, Référence #YYY -->
Closes #

## 🧪 Tests effectués

- [ ] `python manage.py test apps.reservations --verbosity=2` — PASS
- [ ] `python manage.py test apps --verbosity=2` — PASS
- [ ] Tests manuels dans le navigateur
- [ ] Tests API avec curl/Postman

## 📸 Captures d'écran (si applicable)

<!-- Avant / Après -->

## 📝 Changements notables

<!-- Liste des modifications importantes -->
- Changement 1
- Changement 2

## ⚠️ Points d'attention pour le reviewer

<!-- Y a-t-il des aspects particuliers à vérifier ? -->

## ✅ Checklist

- [ ] Mon code respecte PEP 8 et les conventions du projet
- [ ] J'ai ajouté des docstrings aux classes et méthodes publiques
- [ ] J'ai ajouté des tests pour les nouveaux comportements
- [ ] Tous les tests existants passent
- [ ] La documentation est mise à jour si nécessaire
- [ ] Les messages de commit suivent Conventional Commits
- [ ] J'ai mis à jour le CHANGELOG.md
- [ ] Pas de `print()` ou `import pdb` oublié dans le code
- [ ] Les secrets/tokens ne sont pas committés
```

---

## 9. Tests obligatoires

### 9.1 Lancer la suite de tests

```bash
# Tests du module principal
python manage.py test apps.reservations --verbosity=2

# Tous les modules
python manage.py test apps --verbosity=2

# Un test spécifique
python manage.py test apps.reservations.tests.AnnulationRemboursementTests

# Avec couverture
coverage run manage.py test apps
coverage report -m
coverage html
```

### 9.2 Résultats attendus

```
Ran 31 tests in 23.391s
OK
```

> ⚠️ **Règle absolue :** Aucune PR n'est acceptée si des tests existants échouent.

### 9.3 Couverture minimale requise

| Module | Couverture minimale |
|--------|:-------------------:|
| `apps.reservations.models` | 90% |
| `apps.reservations.views` | 75% |
| `apps.reservations.pdf_generator` | 70% |
| `apps.reservations.email_service` | 70% |

---

## 10. Checklist avant soumission

### Développeur

```
Avant de créer la Pull Request, vérifiez :

Code Quality
  ✅ Code PEP 8 conforme
  ✅ Pas de code mort (print, commentaires inutiles)
  ✅ Docstrings sur toutes les classes/méthodes publiques
  ✅ Pas de secrets/tokens dans le code

Tests
  ✅ python manage.py test apps.reservations → OK
  ✅ python manage.py check → 0 issues
  ✅ Nouveaux tests ajoutés pour la feature
  ✅ Tests manuels validés dans le navigateur

Git
  ✅ Branche nommée selon la convention (feat/, fix/, etc.)
  ✅ Commits avec Conventional Commits format
  ✅ Pas de fichiers sensibles committés (.env, db.sqlite3)
  ✅ PR cible la branche develop

Documentation
  ✅ CHANGELOG.md mis à jour
  ✅ README mis à jour si nouvelle feature majeure
  ✅ Docstrings à jour
```

---

## 🛡️ Sécurité

### Signaler une vulnérabilité de sécurité

> ⚠️ **NE PAS** créer d'issue publique pour les vulnérabilités de sécurité.

Envoyez un email à : **security@transport-reservation.com**

Incluez :
- Description de la vulnérabilité
- Étapes de reproduction
- Impact potentiel
- Suggestions de correction (optionnel)

Vous recevrez une réponse dans les **48 heures ouvrables**.

---

<div align="center">

*[← Changelog](08_CHANGELOG.md) • [Plan de Déploiement →](10_PLAN_DEPLOIEMENT.md)*

</div>
