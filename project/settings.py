from project.settings_mobius import *


# Our app must be first
INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS = ["skeleton"] + INSTALLED_APPS

# Configuration for our app
SKELETON = {
}

# settings_local.py is a convenient place to do extra configuration during
# development.  However, it is not the right place to set debug - use the .env
# file for that.
try:
    import project.settings_local as settings_local
    from project.settings_local import *
except ImportError:
    pass
else:
    if hasattr(settings_local, "configure"):
        lcl = locals()
        di = settings_local.configure(**locals())
        lcl.update(**di)
