import os
import raven


# Declare or redeclare variables here
FOOFOO = 1

# You should redefine the CACHE setting here

# Configure raven. Set "dsn" to None for your development environment.
RAVEN_CONFIG = {
    "dsn": None
#    "dsn": "https://<key>:<secret>@sentry.io/<project>",
}


# If you need to access an existing variable your code must be in configure
def configure(**kwargs):
    return {"BARBAR": kwargs["MEDIA_URL"] + "XXX"}
