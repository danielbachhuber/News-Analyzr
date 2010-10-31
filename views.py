from django.shortcuts import render_to_response
from django.template import RequestContext

from organizations.models import *

def homepage(request):
    
    recently_updated_orgs = Organization.objects.order_by('-modified')[:10]

    return render_to_response('homepage.html', {
        'recently_updated_orgs': recently_updated_orgs,
    }, context_instance=RequestContext(request))