from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField, AutoSlugField
from revisions.models import VersionedModel

class ContentBase(models.Model):
    uuid = UUIDField(version=4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class NamedContentBase(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

class VersionedContentBase(VersionedModel):
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User)

    class Meta:
        abstract = True