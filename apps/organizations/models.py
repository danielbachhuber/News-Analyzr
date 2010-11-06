from django.db import models
from apps.dbpedia import models as dbpedia_models
from apps.products.models import *
from django_extensions.db.fields import UUIDField, AutoSlugField

class OrganizationType(models.Model):
    uuid = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Organization(models.Model):
    uuid = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    homepage = models.URLField(blank=True)
    address = models.TextField(blank=True)

    organization_type = models.ForeignKey(OrganizationType)

    parents = models.ManyToManyField('self', blank=True)

    dbpedia = models.ForeignKey(dbpedia_models.NewsOrg, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('organization_detailed', (), {
            'slug': self.slug,
        })
        
    @models.permalink
    def get_edit_url(self):
        return ('organization_edit', (), {
            'slug': self.slug,
        })
