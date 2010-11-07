from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from apps.organizations.models import *

def organization_list(request):
    
    organization_list = Organization.objects.order_by('name')
    
    paginator = Paginator(organization_list, 25) # Show 25 organizations per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        organizations = paginator.page(page)
    except (EmptyPage, InvalidPage):
        organizations = paginator.page(paginator.num_pages)
    
    return render_to_response('organizations/organization_list.html', {
        'organizations': organizations,
    }, context_instance=RequestContext(request))
    
def organization_detailed(request, slug):
    
    organization = get_object_or_404(Organization, slug=slug)
    
    return render_to_response('organizations/organization_detailed.html', {
        'organization': organization,
    }, context_instance=RequestContext(request))
    
def organization_edit(request):
    pass