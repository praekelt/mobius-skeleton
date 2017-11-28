import os
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"

from channels.asgi import get_channel_layer
channel_layer = get_channel_layer()
