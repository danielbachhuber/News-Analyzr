from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from apps.organizations.models import *

def organization_list(request):
    pass
    
def organization_detailed(request, slug):
    
    organization = get_object_or_404(Organization, slug=slug)
    
    return render_to_response('organizations/organization_detailed.html', {
        'organization': organization,
    }, context_instance=RequestContext(request))
    
def organization_edit(request):
    pass