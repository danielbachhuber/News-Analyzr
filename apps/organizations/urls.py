from django.conf.urls.defaults import *

from models import Organization

urlpatterns = patterns('',
    
    # Edit an organization
    url(r'^organizations/(?P<slug>[-\w]+)/edit/$', 'apps.organizations.views.organization_edit', name='organization_edit'),
    # Detailed organization
    url(r'^organizations/(?P<slug>[-\w]+)/$', 'apps.organizations.views.organization_detailed', name='organization_detailed'),
    # All organizations listing
    url(r'^organizations/$', 'apps.organizations.views.organization_list', name='organization_list')
    
)
