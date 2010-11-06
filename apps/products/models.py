from django.db import models
from apps.organizations import models as organization_models
from django_extensions.db.fields import UUIDField, AutoSlugField

class ProductType(models.Model):
    uuid = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Product(models.Model):
    uuid = UUIDField(version=4, primary_key=True)
    organization = models.ForeignKey(organization_models.Organization)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    homepage = models.URLField(blank=True)

    product_type = models.ForeignKey(ProductType)

    daylife_source = models.CharField(max_length=16, blank=True)

    def __unicode__(self):
        return self.name