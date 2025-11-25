from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-reemplaza-esto-por-una-clave-real'

DEBUG = True

ALLOWED_HOSTS = []


# -----------------------------
#    APPS INSTALADAS
# -----------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tu app debe cargar signals → usar la configuración
    'expresos.apps.ExpresosConfig',
]


# -----------------------------
#    MIDDLEWARE
# -----------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------------
#    URL PRINCIPAL
# -----------------------------

ROOT_URLCONF = 'tes_express.urls'


# -----------------------------
#    TEMPLATES
# -----------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # carpetas templates globales
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# -----------------------------
#    WSGI
# -----------------------------

WSGI_APPLICATION = 'tes_express.wsgi.application'


# -----------------------------
#    BASE DE DATOS
# -----------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -----------------------------
#    VALIDADORES
# -----------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# -----------------------------
#    CONFIGURACIÓN DE IDIOMA
# -----------------------------

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Guayaquil'

USE_I18N = True
USE_TZ = True


# -----------------------------
#    ARCHIVOS ESTÁTICOS
# -----------------------------

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


# -----------------------------
#    CLAVE PRIMARIA
# -----------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------
#    LOGIN / LOGOUT
# -----------------------------

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
