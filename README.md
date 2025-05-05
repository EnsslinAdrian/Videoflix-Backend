
# 🎬 Videoflix Backend – Installationsanleitung

Willkommen im **Videoflix Backend**!

Diese Anleitung erklärt Schritt für Schritt, wie du das Backend lokal auf einem Ubuntu- oder WSL-System installierst und startest. Nach dieser Anleitung läuft dein Projekt mit PostgreSQL, Redis, Django, RQ Worker und einer .env Konfigurationsdatei.

---

## 📝 Voraussetzungen

Bitte installiere:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip postgresql postgresql-contrib redis git
```

Optional: Docker (nur wenn du Redis lieber in Docker starten willst).

---

## 🚀 Projekt klonen

```bash
git clone <DEIN-REPOSITORY-LINK>
cd videoflix_backend
```

---

## 🐍 Virtuelle Umgebung einrichten

```bash
python3 -m venv env
source env/bin/activate
```

---

## 📦 Abhängigkeiten installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🐘 PostgreSQL-Datenbank einrichten

1. PostgreSQL starten:

```bash
sudo service postgresql start
```

2. PostgreSQL-Konsole öffnen:

```bash
sudo -u postgres psql
```

3. Neuen Benutzer & Datenbank erstellen:

```sql
CREATE DATABASE videoflix_db;
CREATE USER videoflix_user WITH PASSWORD 'sicheres_passwort';
ALTER ROLE videoflix_user SET client_encoding TO 'utf8';
ALTER ROLE videoflix_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE videoflix_db TO videoflix_user;
\q
```

Merken: Benutzername: `videoflix_user`, Passwort: `sicheres_passwort`

---

## ⚙️ .env Datei erstellen

Im Projektverzeichnis eine Datei `.env` erstellen:

```bash
touch .env
```

Inhalt der .env:

```plaintext
DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=sicheres_passwort
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=foobared

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=dein_emailbenutzer
EMAIL_PASSWORD=dein_emailpasswort
EMAIL_USE_TLS=True

SECRET_KEY=dein_geheimer_schlüssel
```

---

## 🛠 Migrationen durchführen

```bash
python manage.py migrate
```

---

## 🧪 Superuser erstellen

```bash
python manage.py createsuperuser
```

---

## 🌐 Django starten

```bash
python manage.py runserver
```

Die App ist dann erreichbar unter: [http://localhost:8000](http://localhost:8000)

---

## 🧵 RQ Worker starten (zweites Terminal)

```bash
source env/bin/activate
python manage.py rqworker default
```

---

## 🔁 Redis-Befehle (falls benötigt)

Redis starten (falls noch nicht läuft):

```bash
sudo service redis-server start
```

---

## ✅ Bereit!

Wenn du alle Schritte ausgeführt hast, sollte dein Backend laufen und bereit für die Entwicklung und Tests sein.
