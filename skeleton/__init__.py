from django.conf import settings

SETTINGS = {}
try:
    SETTINGS.update(settings.SKELETON)
except AttributeError:
    # No overrides
    pass
