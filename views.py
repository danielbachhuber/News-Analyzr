from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count

from apps.organizations.models import *

def homepage(request):

    recently_updated_orgs = Organization.objects.order_by('-modified')[:10]
    largest_parents = Organization.objects.annotate(child_count=Count('children')).order_by('-child_count')[:20]

    return render_to_response('homepage.html', {
        'recently_updated_orgs': recently_updated_orgs,
        'largest_parents': largest_parents,
    }, context_instance=RequestContext(request))