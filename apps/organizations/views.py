from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseForbidden
import json

from apps.organizations.models import *
from apps.organizations.forms import *

def organization_list(request):
    
    organization_list = Organization.objects.order_by('name')
    organization_types = OrganizationType.objects.all()
    
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
        'organization_types': organization_types,
    }, context_instance=RequestContext(request))
 
def organization_detailed(request, slug):
    
    organization = get_object_or_404(Organization, slug=slug)    
    
    if request.user.is_authenticated():
        basic_info_form = OrganizationBasicInfoForm(instance=organization)
    else:
        basic_info_form = False
    
    return render_to_response('organizations/organization_detailed.html', {
        'organization': organization,
        'basic_info_form': basic_info_form,
    }, context_instance=RequestContext(request))
    
def organization_edit_basic_info(request, slug):

    if request.method == 'POST' and request.user.is_authenticated():
        organization = get_object_or_404(Organization, slug=slug)   
        form = OrganizationBasicInfoForm(request.POST, instance=organization)
        if form.is_valid():
            updated_organization = form.save(commit=False)
            updated_organization.modified_by = request.user
            updated_organization.save()
            return HttpResponse(json.dumps({
                'status': 'ok',
                'homepage': updated_organization.homepage,
            }), mimetype="application/javascript")

    return HttpResponseForbidden()