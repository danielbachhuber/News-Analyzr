from django.conf.urls.defaults import *
from views import homepage

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mediabase/', include('mediabase.foo.urls')),
    
    # Organization directory and singular organiation URLs
    (r'^organizations/', include('organizations.urls')),

    # Homepage
    url(r'^$', homepage, name='homepage' ),

    # Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
