from django.contrib			import admin
from organizations.models	import *

class OrganizationTypeAdmin(admin.ModelAdmin):
	list_display = ['name', 'description']
	pass

class OrganizationAdmin(admin.ModelAdmin):
	list_display = ['name', 'homepage', 'organization_type', 'modified']
	search_fields = ['name']
	pass
	
admin.site.register(OrganizationType, OrganizationTypeAdmin)	
admin.site.register(Organization, OrganizationAdmin)