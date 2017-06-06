from project.settings_mobius import *


# Our app must be first
INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS = ["skeleton"] + INSTALLED_APPS

# Configuration for our app
SKELETON = {
}

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
if not DEBUG:
    loaders = TEMPLATES[0]["OPTIONS"]["loaders"]
    TEMPLATES[0]["OPTIONS"]["loaders"] = \
        [("django.template.loaders.cached.Loader", loaders)]

# settings_local probably changes the value of DEBUG, so put all code dependent
# on the DEBUG value below this comment.
