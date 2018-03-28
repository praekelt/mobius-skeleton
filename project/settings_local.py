# This file is useful during development and must never be checked in.

import os


# NB: do not set DEBUG here. Some settings depend on it and setting it here has
# no effect. Edit an .env file and set it there. See
# https://django-environ.readthedocs.io/en/latest/ for details.

# Declare or redeclare variables here
FOOFOO = 1

# Uncomment to use PostgreSQL as database or set in an .env file
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "skeleton",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "5432",
        "CONN_MAX_AGE": 600
    }
}
"""

# Uncomment to use memcache as caching backend or set in an .env file
"""
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
        "KEY_PREFIX": "skeleton",
    },
}
"""

# Uncomment if you are doing performance profiling with Django Debug Toolbar
"""
DEBUG_TOOLBAR_PANELS = [
    "ddt_request_history.panels.request_history.RequestHistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]
INTERNAL_IPS = ["127.0.0.1"]
RESULTS_CACHE_SIZE = 20000
"""

# If you need to access an existing variable your code must be in configure
def configure(**kwargs):
    # Uncomment if you are doing performance profiling with Django Debug Toolbar
    """
    return {
        "INSTALLED_APPS": kwargs["INSTALLED_APPS"] + ["debug_toolbar"],
        "MIDDLEWARE_CLASSES": (
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ) + kwargs["MIDDLEWARE_CLASSES"]
    }
    """
    return {}
