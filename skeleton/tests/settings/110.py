import os
import glob
from os.path import expanduser


BASE_DIR = os.path.join(
    glob.glob(os.environ["VIRTUAL_ENV"] +  "/lib/*/site-packages")[0],
    "skeleton"
)

SECRET_KEY = "SECRET_KEY_PLACEHOLDER"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    # The order is important
    "skeleton",
    "mobius",
    "jmbo",
    "photologue",
    "category",
    "django_comments",
    "form_renderers",
    "formtools",
    "likes",
    "link",
    "listing",
    "mote",
    "navbuilder",
    "formfactory",
    "pagination",
    "post",
    "preferences",
    "secretballot",
    "simplemde",
    "sites_groups",
    "composer",
    # TODO: Remove nested_admin once the UI is built
    "nested_admin",

    # Django apps can be alphabetic
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # These apps have no templates
    "cache_headers",
    "celery",
    "crum",
    "layers",
    "raven.contrib.django.raven_compat",
    "rest_framework",
    "rest_framework_extras",
    "ultracache",
    "webpack_loader",
)

MIDDLEWARE_CLASSES = (
    "cache_headers.middleware.CacheHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "composer.middleware.ComposerFallbackMiddleware",
    "likes.middleware.SecretBallotUserIpUseragentMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "crum.CurrentRequestUserMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "composer.context_processors.slots",
                "preferences.context_processors.preferences_cp"
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "mote.loaders.app_directories.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
        },
    },
]

ROOT_URLCONF = "skeleton.tests.urls"

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "test",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

SITE_ID = 1

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_METADATA_CLASS": "rest_framework.metadata.SimpleMetadata",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ),
}

MEDIA_ROOT = "%s/media/" % BASE_DIR
MEDIA_URL = "/media/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
         "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
         }
     },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "WARN",
            "class": "logging.StreamHandler",
            "formatter": "verbose"
        },
        "sentry": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "raven.contrib.django.handlers.SentryHandler",
        },
    },
    "loggers": {
        "raven": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": True,
        },
        "sentry.errors": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": "WARN",
            "propagate": False,
        },
    },
}

# Dummy cache is the default
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "skeleton/generated_statics/bundles/",
        "STATS_FILE": os.path.join(BASE_DIR, "static",
                                   "skeleton", "generated_statics",
                                   "bundles",
                                   "skeleton-website-bundlemap.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [".+\.hot-update.js", ".+\.map"]
    }
}

# Celery runs synchronously for tests
CELERY_TASK_ALWAYS_EAGER = True
