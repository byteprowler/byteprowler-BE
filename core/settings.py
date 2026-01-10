from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# Core
# ------------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DEBUG = (os.getenv("DEBUG", "0").strip() == "1")

# Fix: Render can sometimes pass ALLOWED_HOSTS="" -> this would become []
# so we fall back to "*"
raw_hosts = (os.getenv("ALLOWED_HOSTS") or "*").strip()
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()]

# ------------------------------------------------------------------------------
# CSRF + CORS
# ------------------------------------------------------------------------------
# Comma-separated list in env, e.g:
# CSRF_TRUSTED_ORIGINS=https://byteprowler.vercel.app,https://your-api.onrender.com
raw_csrf = (os.getenv("CSRF_TRUSTED_ORIGINS") or "").strip()
CSRF_TRUSTED_ORIGINS = [o.strip() for o in raw_csrf.split(",") if o.strip()]

# If you want to configure CORS via env, set:
# CORS_ALLOWED_ORIGINS=https://byteprowler.vercel.app,https://www.byteprowler.com,http://localhost:3000
raw_cors = (os.getenv("CORS_ALLOWED_ORIGINS") or "").strip()

DEFAULT_CORS_ALLOWED = [
    "https://byteprowler.vercel.app",
    "https://www.byteprowler.com",
    "http://localhost:3000",
]

CORS_ALLOWED_ORIGINS = (
    [o.strip() for o in raw_cors.split(",") if o.strip()]
    if raw_cors
    else DEFAULT_CORS_ALLOWED
)

# Set to 1 only if you truly want any origin allowed (not recommended)
CORS_ALLOW_ALL_ORIGINS = (os.getenv("CORS_ALLOW_ALL_ORIGINS", "0").strip() == "1")

# Usually keep this False for public APIs like contact forms
CORS_ALLOW_CREDENTIALS = False

# ------------------------------------------------------------------------------
# Apps
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    # local
    "contact",
]

# ------------------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # CORS should be as high as possible (before CommonMiddleware)
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "core.wsgi.application"

# ------------------------------------------------------------------------------
# Database (SQLite OK for simple contact API)
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ------------------------------------------------------------------------------
# Static files (WhiteNoise)
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------------------------------------------------------
# Email (Gmail SMTP)
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = (os.getenv("EMAIL_USE_TLS", "1").strip() == "1")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "")
CONTACT_RECEIVER_EMAIL = os.getenv("CONTACT_RECEIVER_EMAIL", EMAIL_HOST_USER or "")

# ------------------------------------------------------------------------------
# DRF + Swagger (drf-spectacular)
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "ByteProwler Contact API",
    "DESCRIPTION": "API for contact form submissions",
    "VERSION": "1.0.0",
}

# ------------------------------------------------------------------------------
# Production safety on Render (recommended)
# ------------------------------------------------------------------------------
# Render sits behind a proxy; this helps Django know original scheme is HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True  # safe with SECURE_PROXY_SSL_HEADER set
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))  # set e.g 86400 later
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# ------------------------------------------------------------------------------
# Defaults
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"