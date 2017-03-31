import os

from project.settings_mobius import *

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME", "mobius-skeleton"),
        "USER": os.environ.get("DB_USER", "mobius-skeleton"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 600
    }
}

# Our app must be first
INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS = ["skeleton"] + INSTALLED_APPS

# Configuration for our app
SKELETON = {
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": os.environ.get("CACHE_LOCATION", "127.0.0.1:11211"),
    }
}

RAVEN_CONFIG = {
    'dsn': os.environ.get("RAVEN_DSN", ""),
}

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "amqp://myuser:mypassword@localhost:5672//")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "amqp://myuser:mypassword@localhost:5672//")

MEDIA_ROOT = "/var/praekelt/media"
STATIC_ROOT = "/var/praekelt/static"

DEBUG = os.environ.get("DEBUG", False)

# Typically used in actual deploys
try:
    import settings_local
    from settings_local import *
except ImportError:
    pass
else:
    if hasattr(settings_local, "configure"):
        lcl = locals()
        di = settings_local.configure(**locals())
        lcl.update(**di)

# Use a cached template loader if not in debug mode
if DEBUG:
    loaders = TEMPLATES[0]["OPTIONS"]["loaders"]
    TEMPLATES[0]["OPTIONS"]["loaders"] = \
        [("django.template.loaders.cached.Loader", loaders)]

# settings_local probably changes the value of DEBUG, so put all code dependent
# on the DEBUG value below this comment.
