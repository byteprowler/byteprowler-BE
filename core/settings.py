from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


def env_list(name, default):
    raw_value = os.getenv(name)
    if not raw_value:
        return default
    return [item.strip() for item in raw_value.split(",") if item.strip()]


DEBUG = env_bool("DEBUG", False)
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-local-development-only"
    else:
        raise RuntimeError("SECRET_KEY environment variable is required.")

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    [
        "byteprowler-contact.onrender.com",
        "localhost",
        "127.0.0.1",
    ],
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "https://byteprowler.vercel.app")

CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS",
    [
        FRONTEND_URL,
        "https://www.byteprowler.com",
        "http://localhost:3000",
    ],
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "")
CONTACT_RECEIVER_EMAIL = os.getenv("CONTACT_RECEIVER_EMAIL", "")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "ByteProwler Contact API",
    "DESCRIPTION": "API for contact form submissions",
    "VERSION": "1.0.0",
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
