from django.db import models

class TwitterAccount(models.Model):
    username = model.CharField(max_length=20)
    
    # Required for all models
    uuid = UUIDField(version=4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name


