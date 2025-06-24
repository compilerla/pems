"""
Django settings for pems project.
"""

from enum import StrEnum
import json
from pathlib import Path
import os

from django.conf import settings


def _filter_empty(ls):
    return [s for s in ls if s]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = _filter_empty(os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split(","))


class RUNTIME_ENVS(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


def RUNTIME_ENVIRONMENT():
    """Helper calculates the current runtime environment from ALLOWED_HOSTS."""

    # usage of django.conf.settings.ALLOWED_HOSTS here (rather than the module variable directly)
    # is to ensure dynamic calculation, e.g. for unit tests and elsewhere this setting is needed
    env = RUNTIME_ENVS.LOCAL
    if any(["*" in host for host in settings.ALLOWED_HOSTS]):
        env = RUNTIME_ENVS.DEV
    return env


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pems.core",
    "pems.districts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "pems.core.middleware.Healthcheck",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pems.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "pems", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pems.core.context_processors.pems_version",
                "pems.core.context_processors.streamlit",
            ],
        },
    },
]

WSGI_APPLICATION = "pems.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

sslmode = os.environ.get("POSTGRES_SSLMODE", "verify-full")
sslrootcert = os.path.join(BASE_DIR, "certs", "aws_global_postgres_ca_bundle.pem") if sslmode == "verify-full" else None

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {"sslmode": sslmode, "sslrootcert": sslrootcert},
    }
}
if RUNTIME_ENVIRONMENT() == RUNTIME_ENVS.DEV:
    postgres_web_secret = os.environ.get("POSTGRESWEB_SECRET")
    db_credentials = json.loads(postgres_web_secret)
    DATABASES["default"].update(
        {
            "NAME": db_credentials.get("dbname"),
            "USER": db_credentials.get("username"),
            "PASSWORD": db_credentials.get("password"),
            "HOST": db_credentials.get("host"),
            "PORT": db_credentials.get("port"),
        }
    )
else:
    DATABASES["default"].update(
        {
            "NAME": os.environ.get("DJANGO_DB_NAME", "django"),
            "USER": os.environ.get("DJANGO_DB_USER", "django"),
            "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOSTNAME", "postgres"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    )


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "pems", "static")]

# use Manifest Static Files Storage by default
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": os.environ.get(
            "DJANGO_STATICFILES_STORAGE", "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
        )
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Streamlit settings
STREAMLIT_URL = os.environ.get("STREAMLIT_URL", "http://localhost:8501")
