from django.core.management.base import BaseCommand

from dbpedia.models import NewsOrg, Owner
from organizations.models import *

from rdflib import Graph
from rdflib.term import URIRef

class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        g = Graph()
        # g.parse('http://dbpedia.org/resource/SourceMedia', format='xml')

        # for trip in g.triples((None, None, None)):
        #     print trip

        company_org_type, created = OrganizationType.objects.get_or_create(name='Company')

        print NewsOrg.objects.exclude(owner='').count()
        for org in NewsOrg.objects.exclude(owner=''):
            owner_url = org.owner
            owner_dbpedia = Owner.from_dbpedia(owner_url)

            name = owner_dbpedia.name or owner_dbpedia.label or owner_url[owner_url.rfind('/')+1:].replace('_', ' ')
            owner, created = Organization.objects.get_or_create(name=name, homepage=owner_dbpedia.homepage, organization_type=company_org_type)

            try:
                print unicode(owner.name)
            except:
                pass

            for o in org.organization_set.all():
                o.parents.add(owner)
