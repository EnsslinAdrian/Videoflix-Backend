
# Videoflix Backend

Ein Django-basiertes Backend für Video-Streaming mit automatischer HLS-Konvertierung und Hintergrundprozessen über Redis Queue (RQ).

## Voraussetzungen

- Python 3.13.1
- PostgreSQL
- Redis
- ffmpeg
- supervisor (für Produktionsumgebungen)

## Installation

### 1️⃣ Repository klonen

```bash
git clone <REPOSITORY-URL>
cd Videoflix-Backend
```

### 2️⃣ Virtuelle Umgebung erstellen und aktivieren

```bash
python -m venv env
source env/bin/activate
```

### 3️⃣ Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4️⃣ PostgreSQL-Datenbank erstellen

Eine neue Datenbank namens `videoflix` und einen Benutzer mit Passwort erstellen. Beispiel:

```bash
sudo -u postgres psql
CREATE DATABASE videoflix;
CREATE USER dein_user WITH PASSWORD 'dein_passwort';
GRANT ALL PRIVILEGES ON DATABASE videoflix TO dein_user;
\q
```

## .env Datei erstellen

Im Hauptverzeichnis eine Datei `.env` anlegen:

```ini
DB_NAME = 'videoflix'
DB_USER = 'dein_user'
DB_PASSWORD = 'dein_passwort'

REDIS_PASSWORD = 'dein_redis_passwort'  # Falls nötig

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.web.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'deine_email'
EMAIL_HOST_PASSWORD = 'dein_email_passwort'
DEFAULT_FROM_EMAIL = 'Videoflix <deine_email>'

SECRET_KEY = 'dein_secret_key'
DEBUG = True
```

## Django vorbereiten

### 5️⃣ Migrationen ausführen

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Superuser anlegen

```bash
python manage.py createsuperuser
```

### 7️⃣ Statische Dateien sammeln

```bash
python manage.py collectstatic
```

## ffmpeg installieren (wenn noch nicht installiert)

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

## Redis installieren (wenn lokal)

```bash
sudo apt install redis
sudo systemctl enable redis
sudo systemctl start redis
```

## Entwicklungsserver starten

```bash
python manage.py runserver
```

## Redis Queue Worker starten

```bash
python manage.py rqworker
```

## Supervisor Beispiel (für RQ Worker in Produktion)

Datei: `videoflix_rqworker.conf`

```ini
[program:videoflix_rqworker]
command=/PFAD/ZUM/env/bin/python /PFAD/ZUM/manage.py rqworker
directory=/PFAD/ZUM/Videoflix-Backend
user=DEIN_USER
autostart=true
autorestart=true
stdout_logfile=/var/log/rqworker.log
stderr_logfile=/var/log/rqworker_error.log
```

Nach dem Anlegen:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start videoflix_rqworker
```

## Wichtige Hinweise

- Vor dem Start des Projekts sicherstellen, dass PostgreSQL und Redis laufen.
- Der Ordner `media/` speichert hochgeladene Videos und Cover. Dieser Ordner sollte existieren oder automatisch erstellt werden.
- Videodateien sollten im MP4-Format hochgeladen werden.

