from django.db import models

from rdflib import Graph
from rdflib.term import URIRef

import json
import urllib
import unicodedata

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
    def from_dbpedia(cls, dbpedia, force=False):
        obj, created = cls.objects.get_or_create(dbpedia=dbpedia)
        if not created and not force:
            return obj

        g = Graph()
        g.parse(dbpedia, format='xml')

        # iterate over graph and extract values that we want
        values = {}
        for trip in g.triples((None, None, None)):
            key = str(trip[1])

            if key == 'http://dbpedia.org/property/redirect':
                redirect_to = unicode(trip[2])
                if redirect_to != dbpedia:
                    obj.delete()
                    return cls.from_dbpedia(redirect_to)

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


        if hasattr(obj, 'postProcess'):
            obj.postProcess()

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

    owner = models.ForeignKey('Owner', null=True, blank=True)
    headquarters = models.ForeignKey('Headquarters', null=True, blank=True)

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
            'type': 'related'
        },
        'http://dbpedia.org/ontology/headquarters': {
            'field': 'headquarters',
            'type': 'related'
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

    def __unicode__(self):
        return self.name

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

class Headquarters(DbpediaBase):
    label = models.CharField(max_length=500, blank=True)
    loc_lat = models.FloatField(null=True, blank=True)
    loc_long = models.FloatField(null=True, blank=True)

    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)

    dbpedia_fields = {
        'http://www.w3.org/2000/01/rdf-schema#label': {
            'field': 'label',
            'type': 'lang'
        },
        'http://www.w3.org/2003/01/geo/wgs84_pos#long': {
            'field': 'loc_long',
            'type': 'value'
        },
        'http://www.w3.org/2003/01/geo/wgs84_pos#lat': {
            'field': 'loc_lat',
            'type': 'value'
        }
    }

    def postProcess(self):
        if self.label and not self.loc_lat:
            url = 'http://where.yahooapis.com/geocode?q=%s&appid=NfeBrn6m&flags=JC' % urllib.quote_plus(unicodedata.normalize('NFKD', self.label).encode('ascii','ignore'))
            print url
            geocode = json.load(urllib.urlopen(url))
            if geocode['ResultSet']['Found'] > 0:
                self.loc_lat = geocode['ResultSet']['Results'][0]['latitude']
                self.loc_long = geocode['ResultSet']['Results'][0]['longitude']
                self.save()

        if self.loc_lat and self.loc_long:
            url = 'http://ws.geonames.org/countrySubdivisionJSON?lat=%s&lng=%s' % (self.loc_lat, self.loc_long)
            codes = json.load(urllib.urlopen(url))
            self.country = codes.get('countryName', '')
            self.region = codes.get('adminName1', '')
            self.save()
