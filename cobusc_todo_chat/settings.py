from project.settings_mobius import *

ULTRACACHE = {}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "/"

AUTH_USER_MODEL = "kopano.PortalUser"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True  # TODO: Remove post demo
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
SOCIALACCOUNT_PROVIDERS = {
    "facebook": {
        "METHOD": "oauth2",
        "SCOPE": [
            "email", "public_profile"
        ],
        "AUTH_PARAMS": {
            "auth_type": "reauthenticate"
        },
        "FIELDS": [
            "id",
            "email",
            "name",
            "first_name",
            "last_name",
            "verified",
            "locale",
            "timezone",
            "link",
            "gender",
            "updated_time"
        ],
        "EXCHANGE_TOKEN": True,
        "LOCALE_FUNC": lambda request: "kr_KR",
        "VERIFIED_EMAIL": False,
        "VERSION": "v2.4"
    },
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    },
    "linkedin_oauth2": {
        "SCOPE": [
            "r_basicprofile",
            "r_emailaddress",
        ],
        "PROFILE_FIELDS": [
            "id",
            "first-name",
            "last-name",
            "email-address",
        ]
    },
    "twitter": {
        # Twitter is enabled, but has no specific config
    }
}

# For social login, the credentials are managed in
# kopano/management/commands/create_social_applications.py
#
# Run `python manage.py create_social_applications.py` to set it up.
# It is an idempotent operation, so you can run it multiple times.
#
# Facebook credentials are managed by the dev@kopano.ai Facebook user
# developers.facebook.com
# SOCIAL_AUTH_FACEBOOK_KEY = "1510186092378853"
# SOCIAL_AUTH_FACEBOOK_SECRET = "f5e444ef4efcf6bbf426f8a6d548b8ef"

# Google credentials are managed by the dev@kopano.ai Google user.
# Client ID: 943877242628-4c7ro5ps7r1r2buju8m2qmpj8kfimpak.apps.googleusercontent.com
# Secret Key: txnyN5oaBjF__KeVa9vLSKjA

# Twitter credentials are managed by the dev@kopano.ai Twitter user.
# https://apps.twitter.com/app/13996826
# Client ID (API Key): lvsK1WzDzuLEtCdoNjlHlVtjq
# Secret: T5UH2zFiWpAFYKSm8ZpAMMjQl3PqIMg6rcekVcNUyuv3Mxfz16

# Linkedin credentials are managed by the dev@kopano.ai LinkedIn user.
# Client ID: 78no2lalv96tl3
# Secret: 8lLcYj2AhD0lWcaW


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
            "channel_capacity": {
                "daphne.response*": 2000,  # Important for stability
                "http.connect": 2000,
                "http.request": 2000,
                "http.response*": 2000,
                "http.disconnect": 2000,
                "websocket.receive": 2000,
                "websocket.send*": 2000,
                "websocket.connect": 2000,
                "websocket.disconnect": 2000,
            },
            "group_expiry": 300  # Default 86400, but recommended to be lower
        },
        "ROUTING": "kopano.routing.channel_routing",
    }
}

REDIS = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}


# Our app must be first
INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS = [
    "kopano",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.twitter",
    "allauth.socialaccount.providers.linkedin_oauth2",

    # Needs to load after allauth.
    "kopano.allauth_wrappers",
    "channels"
] + INSTALLED_APPS

# Configuration for our app
KOPANO = {
    "business_api": {
        "url": "http://api.kopano.retrotest.co.za",
        #"url": "http://localhost",
        "timeout": 10.0  # In seconds
    },
    "feersum": {
        "channel": "5f225dc5787544b8b4cda513abcbbb6e",
        #"channel": "cobusc-kopano-test",
        "timeout": 10.0,  # In seconds
    }
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
