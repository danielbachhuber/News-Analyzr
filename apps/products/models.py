from django.db import models

from apps.base.models import *
from apps.feeds.models import *
from apps.twitter.models import *
from apps.facebook.models import *

class ProductType(NamedContentBase, ContentBase):
    # uuid, name, slug, created, modified
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Product(VersionedContentBase, NamedContentBase):
    # id, vid, name, slug, modified, modified_by
    organization = models.ForeignKey('organizations.Organization')
    homepage = models.URLField(blank=True)

    product_type = models.ForeignKey(ProductType)

    daylife_source = models.CharField(max_length=16, blank=True)

    feeds = models.ManyToManyField(Feed, related_name='products', blank=True)
    twitter_accounts = models.ManyToManyField(TwitterAccount, related_name='products', blank=True)
    facebook_pages = models.ManyToManyField(FacebookPage, related_name='products', blank=True)
