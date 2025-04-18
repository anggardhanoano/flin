"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
from corsheaders.defaults import default_headers
import dj_database_url

from commons.secret_manager import SecretManager

secret = SecretManager()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.get_env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(secret.get_env("DEBUG", 0)) > 0

ALLOWED_HOSTS = ["*"]

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# TODO
MODULE_APPS = [
    "identities",
    "commons",
    "leads",
]

# TODO
LIBRARY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
]

INSTALLED_APPS = DJANGO_APPS + LIBRARY_APPS + MODULE_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # TODO
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(default=secret.get_env("DATABASE_URL"), conn_max_age=600)
}


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
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
FORM_RENDERER = "django.forms.renderers.DjangoTemplates"

AUTHENTICATION_BACKENDS = ["identities.backend.CustomModelBackend"]
AUTH_USER_MODEL = "identities.User"

# TODO
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5173",
    "http://web:5173",
    "http://localhost",
]

# TODO
CORS_ALLOWED_ORIGIN_REGEXES = []

CORS_ALLOW_CREDENTIALS = True

# TODO
CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-special-request",
    "traceparent"
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 25,
    "EXCEPTION_HANDLER": "commons.exception_handler.custom_exception_handler",
    "DATE_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",
    "DATE_INPUT_FORMATS": [
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ],
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",
    "DATETIME_INPUT_FORMATS": [
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ],
}

GOOGLE_CONFIG = {"CLIENT_ID_MOBILE": secret.get_env(
    "GOOGLE_CLIENT_ID_MOBILE", "")}

AWS_CONFIG = secret.get_bulk_env(
    ["ACCESS_KEY_ID", "SECRET_ACCESS_KEY", "REGION_NAME"], "AWS")

# TODO
S3_CONFIG = secret.get_bulk_env(
    ["BUCKET_GENERAL_PUBLIC"], "S3"
)

SES_CONFIG = secret.get_bulk_env(
    ["REGION_NAME", "REGION_ENDPOINT"], "SES"
)

EMAIL_BACKEND = "django_ses.SESBackend"
AWS_SES_REGION_NAME = SES_CONFIG.get('REGION_NAME')
AWS_SES_REGION_ENDPOINT = SES_CONFIG.get('REGION_ENDPOINT')

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}
