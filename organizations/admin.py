from django.contrib			import admin
from organizations.models	import *

class OrganizationAdmin(admin.ModelAdmin):
	list_display = ['name', 'homepage', 'organization_type', 'modified']
	search_fields = ['name']
	pass
	
admin.site.register(Organization, OrganizationAdmin)