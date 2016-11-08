from django.conf import settings


try:
    SETTINGS = settings.SKELETON
except AttributeError:
    SETTINGS = {}
