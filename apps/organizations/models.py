from django.db import models

from apps.base.models import *
from apps.dbpedia import models as dbpedia_models
from apps.organizations.utils import *

class OrganizationType(NamedContentBase, ContentBase):
    # uuid, name, slug, created, modified
    description = models.TextField()

class Organization(VersionedContentBase, NamedContentBase):
    # id, vid, name, slug, modified, modified_by
    homepage = models.URLField(blank=True)
    address = models.TextField(blank=True)

    organization_type = models.ForeignKey(OrganizationType)

    parents = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='children')

    dbpedia = models.ForeignKey(dbpedia_models.NewsOrg, null=True, blank=True)

    @property
    def long_description(self):
        return generate_long_description(self)

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
