from django.db import models
from django_extensions.db.fields import UUIDField, AutoSlugField

class TwitterAccount(models.Model):
    username = models.CharField(max_length=20)
    twitter_id = models.PositiveIntegerField(blank=True, null=True)
    
    # Required for all models
    uuid = UUIDField(version=4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.username

