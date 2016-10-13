# Declare or redeclare variables here
FOOFOO = 1


# If you need to access an existing variable your code must be in configure
def configure(**kwargs):
    return {"BARBAR": kwargs["MEDIA_URL"] + "XXX"}
