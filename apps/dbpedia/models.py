from django.db import models

from rdflib import Graph
from rdflib.term import URIRef

class Literal(models.Model):
    lang = models.CharField(max_length=5)
    text = models.TextField()

class Value(models.Model):
    value = models.TextField()

class DbpediaBase(models.Model):
    dbpedia = models.URLField(unique=True)

    class Meta:
        abstract = True

    @classmethod
    def from_dbpedia(cls, dbpedia):
        obj, created = cls.objects.get_or_create(dbpedia=dbpedia)
        if not created:
            return obj

        g = Graph()
        g.parse(dbpedia, format='xml')

        # iterate over graph and extract values that we want
        values = {}
        for trip in g.triples((None, None, None)):
            key = str(trip[1])
            field = cls.dbpedia_fields.get(key, None)
            if field:
                if field['type'] == 'value' or field['type'] == 'related':
                    values[key] = trip[2]
                elif field['type'] == 'lang':
                    if trip[2].language == 'en':
                        values[key] = trip[2]
                else:
                    if key not in values:
                        values[key] = []
                    values[key].append(trip[2])

        # populate non-M2M fields
        for key, field in cls.dbpedia_fields.items():
            if (field['type'] == 'value' or field['type'] == 'lang') and key in values:
                setattr(obj, field['field'], unicode(values[key]))

            elif field['type'] == 'related' and key in values:
                related_model = obj._meta.get_field(field['field']).related.parent_model
                setattr(obj, field['field'], related_model.from_dbpedia(unicode(values[key])))

        obj.save()

        # populate M2M fields
        for key, field in cls.dbpedia_fields.items():
            if field['type'] == 'valuelist' and key in values:
                ids = []
                for value in values[key]:
                    m2m = Value(value=unicode(value))
                    m2m.save()
                    ids.append(m2m.id)
                    getattr(obj, field['field']).add(m2m)
                getattr(obj, field['field']).exclude(id__in=ids).delete()

        return obj

class NewsOrg(DbpediaBase):
    wikipedia = models.URLField(blank=True)
    homepage = models.URLField(blank=True)

    name = models.CharField(max_length=500)
    label = models.CharField(max_length=500)
    abstract = models.TextField()

    format = models.ForeignKey('PrintFormat', null=True)
    language = models.ForeignKey('Language', null=True)
    circulation = models.PositiveIntegerField(null=True)

    owner = models.URLField(blank=True)
    headquarters = models.URLField(blank=True)

    links = models.ManyToManyField(Value, related_name='newsorg_links')

    def __unicode__(self):
        return self.dbpedia

    def name(self):
        return self.names.get(lang='en')

    dbpedia_fields = {
        'http://xmlns.com/foaf/0.1/page': {
            'field': 'wikipedia',
            'type': 'value'
        },
        'http://xmlns.com/foaf/0.1/homepage': {
            'field': 'homepage',
            'type': 'value'
        },
        'http://dbpedia.org/ontology/owner': {
            'field': 'owner',
            'type': 'value'
        },
        'http://dbpedia.org/ontology/headquarters': {
            'field': 'headquarters',
            'type': 'value'
        },
        'http://dbpedia.org/ontology/language': {
            'field': 'language',
            'type': 'related'
        },
        'http://dbpedia.org/ontology/circulation': {
            'field': 'circulation',
            'type': 'value'
        },
        'http://dbpedia.org/ontology/format': {
            'field': 'format',
            'type': 'related'
        },
        'http://xmlns.com/foaf/0.1/name': {
            'field': 'name',
            'type': 'lang'
        },
        'http://www.w3.org/2000/01/rdf-schema#label': {
            'field': 'label',
            'type': 'lang'
        },
        'http://dbpedia.org/ontology/abstract': {
            'field': 'abstract',
            'type': 'lang'
        },
        'http://dbpedia.org/property/reference': {
            'field': 'links',
            'type': 'valuelist'
        }
    }

class Language(DbpediaBase):
    label = models.CharField(max_length=500)

    def __unicode__(self):
        return self.label

    dbpedia_fields = {
        'http://www.w3.org/2000/01/rdf-schema#label': {
            'field': 'label',
            'type': 'lang'
        },
    }

class PrintFormat(DbpediaBase):
    label = models.CharField(max_length=500)

    def __unicode__(self):
        return self.label

    dbpedia_fields = {
        'http://www.w3.org/2000/01/rdf-schema#label': {
            'field': 'label',
            'type': 'lang'
        },
    }

class Owner(DbpediaBase):
    name = models.CharField(max_length=500, blank=True)
    label = models.CharField(max_length=500, blank=True)
    homepage = models.URLField(blank=True)

    dbpedia_fields = {
        'http://xmlns.com/foaf/0.1/name': {
            'field': 'name',
            'type': 'lang'
        },
        'http://www.w3.org/2000/01/rdf-schema#label': {
            'field': 'label',
            'type': 'lang'
        },
        'http://xmlns.com/foaf/0.1/homepage': {
            'field': 'homepage',
            'type': 'value'
        },
    }