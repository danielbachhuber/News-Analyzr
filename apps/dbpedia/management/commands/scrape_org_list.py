from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.dbpedia.models import NewsOrg
from apps.organizations.models import *
from apps.products.models import *
from apps.activities.models import *

from rdflib import Graph
from rdflib.term import URIRef

class Command(BaseCommand):
    help = "Scrape DBpedia for all news organizations."

    def handle(self, *args, **options):
        url = 'http://dbpedia.org/ontology/Newspaper'

        g = Graph()
        g.parse(url, format='xml')

        count = 0

        news_org_type, created = OrganizationType.objects.get_or_create(name='News')
        company_org_type, created = OrganizationType.objects.get_or_create(name='Company')
        web_product_type, created = ProductType.objects.get_or_create(name='Website')

        try:
            bot_user = User.objects.get(username='importbot')
        except User.DoesNotExist:
            bot_user = User.objects.create_user('importbot', 'importbot@newsanalyzr.com', 'importbot')
            bot_user.active = False
            bot_user.save()

        for trip in g.triples((None, None, URIRef('http://dbpedia.org/ontology/Newspaper'))):
            url = str(trip[0])
            org = NewsOrg.from_dbpedia(url)

            if Organization.objects.filter(homepage=org.homepage).count() == 0 and Organization.objects.filter(name=org.label).count() == 0:
                new_org = Organization()
                new_org.name = org.label
                new_org.homepage = org.homepage
                new_org.organization_type = news_org_type
                new_org.dbpedia = org
                new_org.modified_by = bot_user
                new_org.save()

                Activity(user=bot_user, content_object=new_org).save()

                if org.owner:
                    data = {'name': unicode(org.owner), 'homepage': org.owner.homepage, 'organization_type': company_org_type}
                    try:
                        owner = Organization.objects.get(**data)
                    except Organization.DoesNotExist:
                        owner = Organization(**data)
                        owner.modified_by = bot_user
                        owner.save(0)
                        Activity(user=bot_user, content_object=owner).save()
                    new_org.parents.add(owner)

                prod = Product()
                prod.organization = new_org
                prod.name = org.label
                prod.homepage = org.homepage
                prod.product_type = web_product_type
                prod.modified_by = bot_user
                prod.save()
                Activity(user=bot_user, content_object=prod).save()

            count += 1
            if count % 10 == 0:
                print count