from django.db import models
from django_extensions.db.fields import UUIDField, AutoSlugField
from apps.base.models import *

class FacebookPage(ContentBase):
    # uuid, created, modified
    url = models.URLField()
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
