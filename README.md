# Videoflix Backend – Lokale Entwicklungsanleitung

Willkommen im Videoflix-Backend! Diese Anleitung erklärt dir (oder anderen Entwicklern), wie du das Projekt lokal zum Laufen bringst – inklusive PostgreSQL, Redis (Docker), Django & RQ Worker.

---

## 📦 Voraussetzungen

Stelle sicher, dass du folgendes installiert hast:

- Python 3.x
- PostgreSQL (über `apt install postgresql`)
- Docker Desktop (läuft im Hintergrund)
- Virtuelle Umgebung eingerichtet (`env/`)

---

## 🚀 Projekt das erste Mal starten

### 1. Repository klonen

```bash
git clone <dein-repo-link>
cd videoflix_backend
```

### 2. Virtuelle Umgebung erstellen und aktivieren

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

---

## 🐘 PostgreSQL starten (Linux / WSL)

```bash
sudo service postgresql start
```

Stelle sicher, dass deine Datenbankverbindung in `settings.py` korrekt ist (z. B. Benutzername, Passwort, DB-Name etc.).

---

## 🐳 Redis mit Docker starten

### Nur beim **ersten Mal**:

```bash
docker run --name redis-local -p 6379:6379 -d redis redis-server --requirepass foobared
```

### Danach (bei jedem Start):

```bash
docker start redis-local
```

---

## ⚙️ Einstellungen prüfen

In `settings.py`:

```python
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': 'foobared',
        'DEFAULT_TIMEOUT': 360,
    }
}
```

---

## 🛠 Migrationen durchführen

```bash
python manage.py migrate
```

---

## 🧪 Superuser erstellen (falls nötig)

```bash
python manage.py createsuperuser
```

---

## 🌐 Django starten

```bash
python manage.py runserver
```

App erreichbar unter: [http://localhost:8000](http://localhost:8000)

---

## 🧵 RQ Worker starten (zweites Terminal)

```bash
source env/bin/activate
python manage.py rqworker default
```

---

## 🔁 Nützliche Docker-Befehle

Redis stoppen:

```bash
docker stop redis-local
```

Redis neu starten:

```bash
docker start redis-local
```

Redis-Container löschen:

```bash
docker rm -f redis-local
```

---

## 🧪 Test-Task

```python
# tasks.py
def say_hello():
    print("Hello from RQ!")
    return "done"
```

```python
# in shell
from django_rq import enqueue
from your_app.tasks import say_hello
enqueue(say_hello)
```

---

## ✅ Bereit!

Wenn du alles oben gemacht hast, ist dein Projekt bereit für die Entwicklung.
