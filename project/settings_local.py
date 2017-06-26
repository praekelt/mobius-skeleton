import os
import raven


# Declare or redeclare variables here
FOOFOO = 1

# You should redefine the CACHE setting here

# Configure raven. Set "dsn" to None for your development environment. It must
# be None - anything else causes problems.
RAVEN_CONFIG = {
    "dsn": None
#    "dsn": "https://<key>:<secret>@sentry.io/<project>",
}

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
