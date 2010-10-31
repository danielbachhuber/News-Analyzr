from django.core.management.base import BaseCommand

from dbpedia.models import NewsOrg
from organizations.models import *

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
        web_product_type, created = ProductType.objects.get_or_create(name='Website')

        for trip in g.triples((None, None, URIRef('http://dbpedia.org/ontology/Newspaper'))):
            url = str(trip[0])
            org = NewsOrg.from_dbpedia(url)

            if Organization.objects.filter(homepage=org.homepage).count() == 0 and Organization.objects.filter(name=org.label).count() == 0:
                new_org = Organization()
                new_org.name = org.label
                new_org.homepage = org.homepage
                new_org.organization_type = news_org_type
                new_org.dbpedia = org
                new_org.save()

                prod = Product()
                prod.organization = new_org
                prod.name = org.label
                prod.homepage = org.homepage
                prod.product_type = web_product_type
                prod.save()


            count += 1
            if count % 10 == 0:
                print count