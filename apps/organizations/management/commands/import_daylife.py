# stdlib
from urlparse import urlsplit

# 3rd party
from xlrd import open_workbook
from django.core.management.base import BaseCommand
from django.db.models import Q

# app
from apps.organizations.models import Organization, OrganizationType
from apps.products.models import Product, ProductType

def normalize_org_name(name):
    name = name.lower()
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
                line[header[colnum].value] = row[colnum].value.strip()
            lines.append(line)
        return lines

    def import_row(self, row):
        """
        {u'URL': u'http://pandorican.wordpress.com/', u'Source ID': u'07yV7Jn6bsa6P', u'Source Rank': 1.0, u'Source Type': u'blog', u'Source Name': u'Pandemonium'}
        """

        # Try to find the Product or Organization, and create records as
        # necessary
        #import pdb;pdb.set_trace()
        product = self.find_product(row)
        if not product:
            org = self.find_organization(row)
            if not org:
                org = self.create_organization(row)
            product = self.create_product(row, org)
        self.add_daylife_data(row, product)


    def find_product(self, row):
        # see if there's a product with the normalized name
        ps = Product.objects.filter(name__iexact=normalize_org_name(row.get('Source Name')))
        if not ps.count():
            #import pdb;pdb.set_trace()
            # see if there's a product with the URL
            urlparts = urlsplit(row.get('Home Page URL', ''))
            if urlparts:
                netloc = urlparts.netloc
            else:
                return

            # XXX: this might match the wrong thing if the original URL contains a slash
            ps = Product.objects.filter(homepage__icontains=netloc)

        if ps.count():
            return ps[0]


    def find_organization(self, row):
        # see if there's a product with the normalized name
        org = Organization.objects.filter(name__iexact=normalize_org_name(row.get('Source Name')))
        if not org.count():
            # see if there's a product with the URL
            urlparts = urlsplit(row.get('Home Page URL', ''))
            #import pdb;pdb.set_trace()
            if urlparts:
                netloc = urlparts.netloc
                top_domain = '.'.join(netloc.split('.')[-2:])
            else:
                return

            # XXX: this might match the wrong thing if the original URL contains a slash
            org = Organization.objects.filter( Q( homepage__icontains='/' + top_domain ) | Q( homepage__icontains='.' + top_domain ) )

        if org.count():
            return org[0]


    def create_organization(self, row):
        #import pdb;pdb.set_trace()
        org = Organization(
                name=row.get('Source Name'),
                homepage=row.get('Home Page URL'),
                # XXX: ew
                organization_type=OrganizationType.objects.get(name='News'),
        )
        org.save()
        return org


    def create_product(self, row, org):
        if 'blog' in row.get('Source Type'):
            ptype = ProductType.objects.get_or_create(name='Blog')[0]
        else:
            ptype = ProductType.objects.get_or_create(name='Website')[0]

        p = Product(
                name=row.get('Source Name'),
                homepage=row.get('Home Page URL'),
                # XXX: ew
                product_type=ptype,
                organization=org,
        )
        p.save()
        return p


    def add_daylife_data(self, row, product):
        product.daylife_source = row.get('Source ID')
        product.save()


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
        for i, row in enumerate(parsed):
            dsi.import_row(row)
            if i % 100 == 0:
                print '. ' + str(i)
