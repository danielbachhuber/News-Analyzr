from django.db import models
from django_extensions.db.fields import UUIDField

class Feed(models.Model):
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
    
    # Required for all models
    uuid = UUIDField(version=4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.url


