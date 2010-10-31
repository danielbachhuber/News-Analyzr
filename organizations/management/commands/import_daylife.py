# stdlib
from urlparse import urlparse

# 3rd party
from xlrd import open_workbook
from django.core.management.base import BaseCommand

# app
from organizations.models import Organization, Product

def normalize_org_name(name):
    name = name.lowercase()
    # TODO: strip stop words: The, etc.
    return name

class DaylifeSourceImporter(object):
    def parse(self, filename):
        wb = open_workbook(filename)
        sheet = wb.sheet_by_index(0)
        header = sheet.row(0)
        lines = []
        for linenum in range(1, sheet.nrows):
            row = sheet.row(linenum)
            line = {}
            for colnum in range(0, len(header)):
                line[header[colnum].value] = row[colnum].value
            lines.append(line)
        return lines
            
    def import_row(self, row):
        """
        {u'URL': u'http://pandorican.wordpress.com/', u'Source ID': u'07yV7Jn6bsa6P', u'Source Rank': 1.0, u'Source Type': u'blog', u'Source Name': u'Pandemonium'}
        """

        # Try to find the Product or Organization, and create records as
        # necessary
        p = self.find_product(row)
        if not p:
            org = self.find_organization(row)
            if not org:
                org = self.create_organization(row)
            p = self.create_product(row, org)


    def find_product(self, row):
        # see if there's a product with the normalized name
        ps = Product.objects.filter(name__iexact=normalize_org_name(row.get('Source Name')))
        if not ps.count():
            # see if there's a product with the URL
            netloc = urlparse.urlsplit(row.get('URL')).netloc
            # XXX: this might match the wrong thing if the original URL contains a slash
            ps = Product.objects.filter(url__icontains=netloc)

        if ps.count():
            return ps[0]


    def find_organization(self, row):
        # see if there's a product with the normalized name
        org = Organization.objects.filter(name__iexact=normalize_org_name(row.get('Source Name')))
        if not org.count():
            # see if there's a product with the URL
            netloc = urlparse.urlsplit(row.get('URL')).netloc
            # XXX: this might match the wrong thing if the original URL contains a slash
            org = Organization.objects.filter(url__icontains=netloc)

        if org.count():
            return org[0]


    def create_organization(self, row):
        org = Organization(
                name=row.get('Source Name'),
                homepage=row.get('URL'),
                # XXX: ew
                organization_type=OrganizationType.objects.get(name='News'),
        )
        org.save()
        return org


    def create_product(self, row, org):
        if 'blog' in row.get('Source Type'):
            ptype = ProductType.objects.get(name='Blog')
        else:
            ptype = ProductType.objects.get(name='Website')

        p = Product(
                name=row.get('Source Name'),
                homepage=row.get('URL'),
                daylife_source=row.get('Source ID'),
                # XXX: ew
                product_type=ptype,
        )
        p.save()
        return p


class Command(BaseCommand):
    args = """<filename>"""
    help = """Creates Organizations and Products from Daylife's master list
    of sources.
    """

    def handle(self, *args, **options):
        filename = args[0]
        if not filename:
            return

        dsi = DaylifeSourceImporter()
        parsed = dsi.parse(filename)
        for row in parsed:
            dsi.import_row(row)
