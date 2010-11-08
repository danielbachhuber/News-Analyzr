from django.conf.urls.defaults import *

from models import Organization

urlpatterns = patterns('',
    
    # Edit an organization
    url(r'^(?P<slug>[-\w]+)/edit_basic_info/$', 'apps.organizations.views.organization_edit_basic_info', name='organization_edit_basic_info'),
    # Detailed organization
    url(r'^(?P<slug>[-\w]+)/$', 'apps.organizations.views.organization_detailed', name='organization_detailed'),
    # All organizations listing
    url(r'^$', 'apps.organizations.views.organization_list', name='organization_list')
    
)
