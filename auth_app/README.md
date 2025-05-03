
# Django Auth App 🔐

Wiederverwendbare Django-App zur Authentifizierung – mit:
- Registrierung + E-Mail-Verifizierung ✅
- Login (JWT) + Refresh ✅
- Passwort-Reset per E-Mail ✅
- Google Social Login ✅
- Profilverwaltung ✅
- Token-basierter Re-Auth ✅



## ⚙️ Einstellungen (`settings.py`)

### Django-Apps
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'auth_app',
]
```

### Django REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

### Benutzerdefiniertes User-Modell
Da die App ein eigenes User-Modell verwendet, musst du in deinen Einstellungen folgendes setzen:

```python
AUTH_USER_MODEL = "auth_app.CustomUser"
```

⚠️ Das **muss vor dem ersten `makemigrations`** geschehen!

---

### E-Mail Backend (für Verifizierung & Passwort-Reset)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.web.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'deine@mailadresse.de'
EMAIL_HOST_PASSWORD = 'dein-passwort'  # 👉 besser über Umgebungsvariable!

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### Frontend-URLs (für Links in E-Mails)
```python
FRONTEND_VERIFY_URL = "http://localhost:4200/email-verifizieren"
FRONTEND_RESET_URL = "http://localhost:4200/passwort-vergessen"
```

---

## 🌐 URL-Konfiguration

In deiner Haupt-`urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('auth_app.api.urls')),
    # ...
]
```

---

## 📁 Templates

Die App bringt bereits E-Mail-Templates mit:

- `templates/verify_email.html`
- `templates/password_reset_email.html`

Du kannst sie bei Bedarf überschreiben oder erweitern.

---

## ✅ Endpunkte (Auszug)

| Endpoint                             | Methode | Beschreibung                    |
|-------------------------------------|---------|---------------------------------|
| `/api/auth/register/`               | POST    | Benutzer registrieren           |
| `/api/auth/verify-email/`           | GET     | E-Mail-Verifizierung            |
| `/api/auth/login/`                  | POST    | Login via E-Mail + Passwort     |
| `/api/auth/social/google/`          | POST    | Login mit Google Token          |
| `/api/auth/password-reset/`         | POST    | Anfrage Passwort-Reset          |
| `/api/auth/password-reset/confirm/` | POST    | Passwort zurücksetzen           |
| `/api/auth/me/`                     | GET/PUT | Aktuelles Benutzerprofil        |
| `/api/auth/logout/`                 | POST    | Logout (Refresh Token löschen)  |

---

## 🧪 Testen

Du kannst die App wie gewohnt mit Django-Tests testen:

```bash
python manage.py test auth_app
```

---

## 🧠 Hinweise

- Authentifizierung läuft über JWT (access + refresh token).
- Refresh-Token wird im Cookie gespeichert (`refresh_token`).
- Re-Authentication (z. B. für "Account löschen") mit Ablaufzeit.
- Google Login benötigt kein OAuth-Setup auf deiner Seite – nur das Google ID Token.

---

## 📄 Lizenz

MIT License – feel free to use and contribute 🚀
