# 🚀 Plan de Déploiement — Transport Réservation v2.0

> **Environnement cible :** Serveur Linux (Ubuntu 22.04 LTS)  
> **Stack :** Gunicorn + Nginx + Django 5.1.4  
> **Base de données :** PostgreSQL 15  
> **Cache :** Redis 7  
> **Version :** 2.0.0 — Novembre 2024

---

## 📑 Table des matières

1. [Vue d'ensemble du déploiement](#1-vue-densemble-du-déploiement)
2. [Prérequis serveur](#2-prérequis-serveur)
3. [Préparation du serveur](#3-préparation-du-serveur)
4. [Installation de l'application](#4-installation-de-lapplication)
5. [Configuration de la base de données](#5-configuration-de-la-base-de-données)
6. [Configuration de l'application](#6-configuration-de-lapplication)
7. [Configuration Gunicorn](#7-configuration-gunicorn)
8. [Configuration Nginx](#8-configuration-nginx)
9. [Configuration Redis (cache)](#9-configuration-redis-cache)
10. [Configuration Email SMTP](#10-configuration-email-smtp)
11. [SSL/HTTPS avec Let's Encrypt](#11-sslhttps-avec-lets-encrypt)
12. [Checklist de sécurité](#12-checklist-de-sécurité)
13. [Déploiement continu (CI/CD)](#13-déploiement-continu-cicd)
14. [Procédures de maintenance](#14-procédures-de-maintenance)
15. [Checklist finale de déploiement](#15-checklist-finale-de-déploiement)

---

## 1. Vue d'ensemble du déploiement

### 1.1 Architecture de production

```
Internet
    │
    ▼
┌─────────────────────────────────────┐
│          Nginx (Port 80/443)         │
│    Reverse proxy + SSL termination  │
│    + Fichiers statiques (Whitenoise) │
└─────────────┬───────────────────────┘
              │  (Port 8000 interne)
              ▼
┌─────────────────────────────────────┐
│     Gunicorn (WSGI Server)          │
│     4 workers × application Django  │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│  PG   │ │ Redis │ │  Logs │
│  DB   │ │ Cache │ │  Dir  │
└───────┘ └───────┘ └───────┘
```

### 1.2 Spécifications serveur recommandées

| Ressource | Minimum | Recommandé |
|-----------|:-------:|:----------:|
| CPU | 2 cœurs | 4 cœurs |
| RAM | 2 Go | 4 Go |
| Stockage | 20 Go SSD | 50 Go SSD |
| OS | Ubuntu 20.04 | Ubuntu 22.04 LTS |
| Python | 3.11 | 3.11+ |

---

## 2. Prérequis serveur

### 2.1 Packages système requis

```bash
# Mise à jour du système
sudo apt-get update && sudo apt-get upgrade -y

# Packages essentiels
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    redis-server \
    git \
    curl \
    build-essential \
    libpq-dev \
    certbot \
    python3-certbot-nginx
```

### 2.2 Vérification des versions

```bash
python3 --version    # Python 3.11.x
psql --version       # psql (PostgreSQL) 15.x
redis-server --version  # Redis server v=7.x
nginx -v             # nginx/1.x.x
```

---

## 3. Préparation du serveur

### 3.1 Créer un utilisateur système dédié

```bash
# Créer l'utilisateur transport (sans accès shell)
sudo useradd --system --group --home /var/www/transport transport

# Créer les répertoires
sudo mkdir -p /var/www/transport
sudo mkdir -p /var/log/transport
sudo mkdir -p /var/www/transport/media
sudo mkdir -p /var/www/transport/static

# Attribuer les permissions
sudo chown -R transport:transport /var/www/transport
sudo chown -R transport:transport /var/log/transport
```

### 3.2 Cloner le dépôt

```bash
# Se placer dans le répertoire web
cd /var/www/transport

# Cloner le dépôt
sudo -u transport git clone https://github.com/votre-org/transport-reservation.git app
cd app
```

### 3.3 Configurer l'environnement virtuel

```bash
# Créer le venv
sudo -u transport python3.11 -m venv /var/www/transport/venv

# Activer le venv
source /var/www/transport/venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances (production)
pip install -r requirements.txt

# Installer les dépendances Redis (pour la production)
pip install django-redis==5.4.0 redis==5.0.7 psycopg2-binary==2.9.9
```

---

## 4. Configuration de la base de données

### 4.1 Créer la base de données PostgreSQL

```bash
# Se connecter à PostgreSQL en tant que postgres
sudo -u postgres psql

# Dans psql :
CREATE DATABASE transport_db;
CREATE USER transport_user WITH PASSWORD 'VotreMotDePasseSecurise123!';
ALTER ROLE transport_user SET client_encoding TO 'utf8';
ALTER ROLE transport_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE transport_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE transport_db TO transport_user;
\q
```

### 4.2 Tester la connexion

```bash
psql -U transport_user -d transport_db -h localhost
# → Entrer le mot de passe
# → Devrait se connecter sans erreur
\q
```

---

## 5. Configuration de l'application

### 5.1 Créer le fichier `.env` de production

```bash
# Générer une clé secrète sécurisée
python3 -c "import secrets; print(secrets.token_urlsafe(50))"

# Créer et éditer .env
sudo -u transport nano /var/www/transport/app/.env
```

**Contenu du fichier `.env` (production) :**

```ini
# ── Application ─────────────────────────────────────────────
SECRET_KEY=votre-cle-secrete-generee-ci-dessus-50-caracteres-minimum
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# ── Base de données PostgreSQL ────────────────────────────────
DATABASE_URL=postgres://transport_user:VotreMotDePasseSecurise123!@localhost:5432/transport_db

# ── Cache Redis ───────────────────────────────────────────────
REDIS_URL=redis://127.0.0.1:6379/0

# ── Email SMTP ────────────────────────────────────────────────
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@votre-domaine.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-application

# ── Fichiers médias ───────────────────────────────────────────
MEDIA_ROOT=/var/www/transport/app/media/
MEDIA_URL=/media/
STATIC_ROOT=/var/www/transport/staticfiles/

# ── Sécurité production ───────────────────────────────────────
SECURE_SSL_REDIRECT=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

### 5.2 Appliquer les migrations

```bash
cd /var/www/transport/app
source /var/www/transport/venv/bin/activate

python manage.py migrate --noinput
```

### 5.3 Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 5.4 Créer le superutilisateur de production

```bash
python manage.py createsuperuser
# → Renseigner : email, prénom, nom, mot de passe fort
```

### 5.5 Vérifier la configuration

```bash
python manage.py check --deploy
# → Doit retourner 0 erreurs critiques
```

---

## 6. Configuration Django (settings.py — production)

### Paramètres critiques à vérifier

```python
# ── Sécurité ─────────────────────────────────────────────────
DEBUG = False  # JAMAIS True en production
SECRET_KEY = config('SECRET_KEY')  # Depuis .env
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# ── Base de données ───────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'transport_db',
        'USER': 'transport_user',
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,  # Connexions persistantes
    }
}

# ── Cache Redis ───────────────────────────────────────────────
REDIS_URL = config('REDIS_URL', default=None)
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

# ── Sécurité HTTPS ────────────────────────────────────────────
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# ── Fichiers statiques (Whitenoise) ──────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Juste après Security
    ...
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 7. Configuration Gunicorn

### 7.1 Créer le fichier de configuration Gunicorn

```bash
sudo -u transport nano /var/www/transport/gunicorn.conf.py
```

**`gunicorn.conf.py` :**

```python
# Gunicorn configuration
bind = "127.0.0.1:8000"
workers = 4                    # 2 × CPU cores
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logs
accesslog = "/var/log/transport/gunicorn_access.log"
errorlog = "/var/log/transport/gunicorn_error.log"
loglevel = "warning"
capture_output = True

# Process naming
proc_name = "transport_gunicorn"

# Graceful restart
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 50

# Permissions
user = "transport"
group = "transport"
```

### 7.2 Créer le service systemd Gunicorn

```bash
sudo nano /etc/systemd/system/transport-gunicorn.service
```

**`transport-gunicorn.service` :**

```ini
[Unit]
Description=Transport Réservation — Gunicorn WSGI Server
After=network.target postgresql.service redis.service
Requires=postgresql.service

[Service]
Type=notify
User=transport
Group=transport
WorkingDirectory=/var/www/transport/app
Environment="PATH=/var/www/transport/venv/bin"
ExecStart=/var/www/transport/venv/bin/gunicorn \
    --config /var/www/transport/gunicorn.conf.py \
    transport_project.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 7.3 Activer et démarrer Gunicorn

```bash
# Recharger systemd
sudo systemctl daemon-reload

# Activer le service (démarrage automatique)
sudo systemctl enable transport-gunicorn

# Démarrer le service
sudo systemctl start transport-gunicorn

# Vérifier le statut
sudo systemctl status transport-gunicorn

# Tester
curl http://127.0.0.1:8000/
```

---

## 8. Configuration Nginx

### 8.1 Créer la configuration Nginx

```bash
sudo nano /etc/nginx/sites-available/transport
```

**`/etc/nginx/sites-available/transport` :**

```nginx
# Redirection HTTP → HTTPS
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

# Configuration principale HTTPS
server {
    listen 443 ssl http2;
    server_name votre-domaine.com www.votre-domaine.com;

    # Certificats SSL (générés par Certbot)
    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Sécurité
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

    # Fichiers statiques (servis directement par Nginx)
    location /static/ {
        alias /var/www/transport/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Fichiers médias (billets PDF)
    location /media/ {
        alias /var/www/transport/app/media/;
        # Restriction : pas d'accès direct aux PDF
        location ~* \.pdf$ {
            internal;
        }
    }

    # Proxy vers Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Buffer
        proxy_buffering on;
        proxy_buffer_size 8k;
        proxy_buffers 8 8k;
    }

    # Taille maximale des uploads
    client_max_body_size 10M;

    # Logs
    access_log /var/log/nginx/transport_access.log;
    error_log /var/log/nginx/transport_error.log;
}
```

### 8.2 Activer le site et redémarrer Nginx

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/transport /etc/nginx/sites-enabled/

# Tester la configuration
sudo nginx -t

# Redémarrer Nginx
sudo systemctl restart nginx

# Activer au démarrage
sudo systemctl enable nginx
```

---

## 9. Configuration Redis (cache)

### 9.1 Configurer Redis

```bash
sudo nano /etc/redis/redis.conf
```

**Modifications dans `redis.conf` :**

```conf
# Lier à localhost uniquement (sécurité)
bind 127.0.0.1

# Mot de passe Redis (optionnel mais recommandé)
requirepass VotreMotDePasseRedis123

# Mémoire maximale (adapter selon RAM disponible)
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistance
save 900 1
save 300 10
save 60 10000
```

### 9.2 Activer et démarrer Redis

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server

# Test
redis-cli ping  # → PONG
```

---

## 10. Configuration Email SMTP

### 10.1 Gmail (App Password)

Pour utiliser Gmail en production :

1. Activer la **vérification en 2 étapes** sur votre compte Google
2. Aller dans **Sécurité → Mots de passe des applications**
3. Générer un mot de passe pour "Autre application" → `Transport Reservation`
4. Utiliser ce mot de passe dans `.env` (16 caractères sans espaces)

### 10.2 Tester la configuration email

```bash
cd /var/www/transport/app
source /var/www/transport/venv/bin/activate

python manage.py shell -c "
from django.core.mail import send_mail
send_mail(
    'Test email Transport Réservation',
    'Configuration email OK.',
    'noreply@votre-domaine.com',
    ['admin@votre-domaine.com'],
    fail_silently=False,
)
print('Email envoyé avec succès !')
"
```

---

## 11. SSL/HTTPS avec Let's Encrypt

### 11.1 Obtenir le certificat SSL

```bash
# Arrêter temporairement Nginx
sudo systemctl stop nginx

# Obtenir le certificat
sudo certbot certonly --standalone \
    -d votre-domaine.com \
    -d www.votre-domaine.com \
    --email admin@votre-domaine.com \
    --agree-tos \
    --non-interactive

# Redémarrer Nginx
sudo systemctl start nginx
```

### 11.2 Renouvellement automatique

```bash
# Tester le renouvellement
sudo certbot renew --dry-run

# Le renouvellement automatique est géré par un timer systemd
sudo systemctl status certbot.timer
```

---

## 12. Checklist de sécurité

### 12.1 Checklist Django

```bash
# Vérification de sécurité Django
python manage.py check --deploy

# Résultat attendu :
# System check identified no issues (0 silenced).
```

### 12.2 Checklist complète

| Critère | Statut | Commande de vérification |
|---------|:------:|--------------------------|
| `DEBUG = False` | ☐ | `grep DEBUG .env` |
| `SECRET_KEY` unique et longue | ☐ | Longueur > 50 chars |
| `ALLOWED_HOSTS` configuré | ☐ | Domaine exact uniquement |
| `HTTPS` actif | ☐ | `curl -I https://votre-domaine.com` |
| `HSTS` activé | ☐ | Header `Strict-Transport-Security` |
| `CSRF_COOKIE_SECURE = True` | ☐ | `python manage.py check --deploy` |
| `SESSION_COOKIE_SECURE = True` | ☐ | `python manage.py check --deploy` |
| `X_FRAME_OPTIONS = 'DENY'` | ☐ | Header `X-Frame-Options` |
| PostgreSQL (pas SQLite) | ☐ | `python manage.py dbshell` |
| Redis configuré | ☐ | `redis-cli ping` |
| Logs en dehors du web root | ☐ | `/var/log/transport/` |
| `.env` hors du repo Git | ☐ | `.gitignore` contient `.env` |
| `media/` hors du repo Git | ☐ | `.gitignore` contient `media/` |
| Pare-feu configuré (UFW) | ☐ | `sudo ufw status` |
| SSH par clé (pas mot de passe) | ☐ | `/etc/ssh/sshd_config` |

### 12.3 Configuration pare-feu (UFW)

```bash
sudo ufw enable
sudo ufw allow ssh      # Port 22
sudo ufw allow 80/tcp   # HTTP (redirigé vers HTTPS)
sudo ufw allow 443/tcp  # HTTPS
sudo ufw deny 8000/tcp  # Gunicorn non accessible directement
sudo ufw status
```

---

## 13. Déploiement continu (CI/CD)

### 13.1 Script de déploiement automatique

```bash
# /var/www/transport/deploy.sh
#!/bin/bash
set -e

echo "═══════════════════════════════════════"
echo "  DÉPLOIEMENT Transport Réservation v2"
echo "═══════════════════════════════════════"

APP_DIR="/var/www/transport/app"
VENV_DIR="/var/www/transport/venv"
STATIC_DIR="/var/www/transport/staticfiles"

# 1. Pull du code
echo "→ Pull du code depuis git..."
cd $APP_DIR
git pull origin main

# 2. Activer le venv et mettre à jour les dépendances
echo "→ Mise à jour des dépendances..."
source $VENV_DIR/bin/activate
pip install -r requirements.txt --quiet

# 3. Migrations
echo "→ Application des migrations..."
python manage.py migrate --noinput

# 4. Collecte des statiques
echo "→ Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# 5. Vérification
echo "→ Vérification de la configuration..."
python manage.py check --deploy

# 6. Redémarrage de Gunicorn (graceful)
echo "→ Redémarrage de Gunicorn..."
sudo systemctl reload transport-gunicorn

echo "✅ Déploiement terminé avec succès !"
echo "   URL : https://votre-domaine.com/"
```

```bash
# Rendre exécutable
sudo chmod +x /var/www/transport/deploy.sh
```

### 13.2 GitHub Actions (CI/CD optionnel)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          python manage.py test apps.reservations --verbosity=2
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: /var/www/transport/deploy.sh
```

---

## 14. Procédures de maintenance

### 14.1 Redémarrage des services

```bash
# Redémarrage complet (si problème critique)
sudo systemctl restart transport-gunicorn
sudo systemctl restart nginx
sudo systemctl restart postgresql
sudo systemctl restart redis-server

# Rechargement sans coupure (recommandé)
sudo systemctl reload transport-gunicorn
sudo systemctl reload nginx
```

### 14.2 Vérification des logs

```bash
# Logs Gunicorn
sudo journalctl -u transport-gunicorn -n 50
tail -f /var/log/transport/gunicorn_error.log

# Logs Nginx
tail -f /var/log/nginx/transport_error.log
tail -f /var/log/nginx/transport_access.log

# Logs applicatifs Django
tail -f /var/www/transport/app/logs/errors.log
tail -f /var/www/transport/app/logs/reservations.log
```

### 14.3 Sauvegarde de la base de données

```bash
#!/bin/bash
# /etc/cron.d/transport-backup

# Sauvegarde quotidienne à 2h du matin
BACKUP_DIR="/var/backups/transport"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Dump PostgreSQL
pg_dump -U transport_user -h localhost transport_db \
    | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Garder 30 jours de sauvegardes
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

echo "Sauvegarde créée : $BACKUP_DIR/db_$DATE.sql.gz"
```

```bash
# Ajouter au crontab
sudo crontab -e
# Ajouter : 0 2 * * * /bin/bash /var/www/transport/backup.sh
```

### 14.4 Mise à jour de l'application

```bash
# Procédure de mise à jour standard
sudo -u transport /var/www/transport/deploy.sh

# Rollback en cas d'erreur
cd /var/www/transport/app
git log --oneline -5      # Voir les 5 derniers commits
git checkout v2.0.0       # Retourner à une version stable
sudo systemctl reload transport-gunicorn
```

---

## 15. Checklist finale de déploiement

### Avant le déploiement

```
□ Tests passent localement : python manage.py test apps.reservations → OK
□ python manage.py check → 0 issues
□ .env de production configuré avec toutes les variables
□ SECRET_KEY unique générée (50+ caractères)
□ DEBUG = False dans .env
□ ALLOWED_HOSTS configuré avec le bon domaine
□ Base de données PostgreSQL créée et testée
□ Redis démarré et accessible
□ Certificat SSL obtenu
□ Gunicorn service configuré et testé
□ Nginx configuré et site activé
□ Pare-feu UFW configuré (ports 22, 80, 443 uniquement)
```

### Pendant le déploiement

```
□ git pull origin main (ou tag de release)
□ pip install -r requirements.txt
□ python manage.py migrate --noinput
□ python manage.py collectstatic --noinput
□ python manage.py check --deploy (0 erreurs critiques)
□ sudo systemctl reload transport-gunicorn
□ curl -I https://votre-domaine.com/ → 200 OK
```

### Après le déploiement

```
□ Page d'accueil accessible : https://votre-domaine.com/
□ Connexion admin fonctionne : https://votre-domaine.com/admin/
□ API accessible : https://votre-domaine.com/api/
□ Billet PDF téléchargeable (test réservation)
□ Email de confirmation reçu
□ Logs sans erreurs critiques : tail -f /var/log/transport/gunicorn_error.log
□ Performance : < 2 secondes de réponse
□ HTTPS actif et certificat SSL valide
□ Header HSTS présent
□ Sauvegarde automatique programmée (cron)
□ Monitoring en place (uptime check)
□ Équipe notifiée du déploiement réussi
```

---

## 📊 Métriques de performance attendues

| Métrique | Développement | Production |
|----------|:-------------:|:----------:|
| Temps de réponse (pages) | < 500ms | < 200ms |
| Temps de réponse (API) | < 200ms | < 100ms |
| Temps de réponse (PDF) | < 3s | < 2s |
| Cache hit ratio | — | > 70% |
| Uptime attendu | — | > 99.5% |
| Backup fréquence | — | Quotidien |

---

<div align="center">

*[← Guide Contribution](09_GUIDE_CONTRIBUTION.md) • [← README Projet](04_README_PROJET.md)*

</div>
