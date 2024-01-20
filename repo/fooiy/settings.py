import boto3
import firebase_admin
from firebase_admin import credentials
from pathlib import Path
from . import env
import os
import pymysql

BASE_DIR = Path(__file__).resolve().parent.parent

#### 파이어베이스 푸시알람 키 ####
credential_path = os.path.join(BASE_DIR, "firebase_service_account_key.json")
credential = credentials.Certificate(credential_path)
firebase_admin.initialize_app(credential)


SECRET_KEY = env.DJANGO_SECRET_KEY
PHASE = env.PHASE

if PHASE == "PROD":
    DEBUG = False
elif PHASE == "ADMIN":
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    "https://fooiy.com",
    "https://www.fooiy.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.5:3000",
]
CORS_ALLOW_CREDENTIALS = True


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    ###########################
    # third party
    ###########################
    # CORS
    "corsheaders",
    # Api Docs
    "drf_yasg",
    # Django Rest Framework
    "rest_framework",
    # Django Storages
    "storages",
    ###########################
    # add APP
    ###########################
    "accounts",
    "shops",
    "archives",
    "feeds",
    "web",
    "ui",
    "search",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "common.fooiy_response.unexpected_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

ROOT_URLCONF = "fooiy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "fooiy.wsgi.application"

pymysql.install_as_MySQLdb()
# Env Setting
if PHASE == "PROD":
    AWS_STORAGE_BUCKET_NAME = "fooiy"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env.DATABASES_DEFAULT_NAME,
            "USER": env.DATABASES_DEFAULT_USER,
            "PASSWORD": env.DATABASES_DEFAULT_PASSWORD,
            "HOST": env.DATABASES_DEFAULT_HOST,
            "PORT": "3306",
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env.CACHES_DEFAULT_HOST,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            },
        },
    }
elif PHASE == "ADMIN":
    AWS_STORAGE_BUCKET_NAME = "fooiy"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env.DATABASES_DEFAULT_NAME,
            "USER": env.DATABASES_DEFAULT_USER,
            "PASSWORD": env.DATABASES_DEFAULT_PASSWORD,
            "HOST": env.DATABASES_DEFAULT_HOST,
            "PORT": "3306",
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env.CACHES_DEFAULT_HOST,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            },
        },
    }
else:
    AWS_STORAGE_BUCKET_NAME = "fooiy-dev"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env.DEV_DATABASES_DEFAULT_NAME,
            "USER": env.DEV_DATABASES_DEFAULT_USER,
            "PASSWORD": env.DEV_DATABASES_DEFAULT_PASSWORD,
            "HOST": env.DEV_DATABASES_DEFAULT_HOST,
            "PORT": "3306",
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env.DEV_CACHES_DEFAULT_HOST,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            },
        },
    }


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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "format1": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "format2": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "format1",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "api": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Slack
SLACK_TOKEN = env.SLACK_TOKEN

# Set Basic User Model
AUTH_USER_MODEL = "accounts.Account"
# Set Basic User Name
ACCOUNT_USER_MODEL_USERNAME_FIELD = "phone_number"
# Set Password Hash Algorithms
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]


# SET Locale
LANGUAGE_CODE = "ko"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# SET Data Size in Network Communication
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000
DATA_UPLOAD_MAX_MEMORY_SIZE = 12621440
FILE_UPLOAD_MAX_MEMORY_SIZE = 12621440

# SET static
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "/static")

SITE_ID = 1

# AWS setting
AWS_ACCESS_KEY_ID = env.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = env.AWS_SECRET_ACCESS_KEY
AWS_REGION = "ap-northeast-2"
AWS_QUERYSTRING_AUTH = False

# S3 Storages
AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = "fooiy.custom_storage.CustomS3Boto3Storage"
S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


# Email smtp Protocol
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = env.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
