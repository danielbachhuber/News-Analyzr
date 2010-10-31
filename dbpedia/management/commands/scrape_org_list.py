from django.core.management.base import BaseCommand

from dbpedia.models import NewsOrg

from rdflib import Graph
from rdflib.term import URIRef

class Command(BaseCommand):
    help = "Scrape DBpedia for all news organizations."

    def handle(self, *args, **options):
        url = 'http://dbpedia.org/ontology/Newspaper'

        g = Graph()
        g.parse(url, format='xml')

        count = 0

        for trip in g.triples((None, None, URIRef('http://dbpedia.org/ontology/Newspaper'))):
            url = str(trip[0])
            NewsOrg.from_dbpedia(url)
            count += 1
            if count % 10 == 0:
                print count