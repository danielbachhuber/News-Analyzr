from django.db import models
from django_extensions.db.fields import UUIDField
from apps.base.models import *

class Feed(ContentBase):
    # uuid, created, modified
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    FORMAT_CHOICES = (
        ('R091', 'RSS 0.91'),
        ('R100', 'RSS 1.0'),
        ('R200', 'RSS 2.0'),
        ('ATOM', 'Atom'),
        ('JSON', 'JSON'),
        ('NITF', 'NITF'),
    )

    format = models.CharField(max_length=4, choices=FORMAT_CHOICES)

    def __unicode__(self):
        return self.url
