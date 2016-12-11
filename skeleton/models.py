from django.db import models

from jmbo.models import ModelBase


class TrivialContent(ModelBase):
    """We need one model so migrations can be initiated."""
