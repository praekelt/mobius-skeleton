import os
import raven


# Declare or redeclare variables here
ALLOWED_HOSTS = ["*"]
FOOFOO = 1

# You should redifine the CACHE setting here

# Configure raven
RAVEN_CONFIG = {
    "dsn": "https://<key>:<secret>@sentry.io/<project>",
}


# If you need to access an existing variable your code must be in configure
def configure(**kwargs):
    return {"BARBAR": kwargs["MEDIA_URL"] + "XXX"}
