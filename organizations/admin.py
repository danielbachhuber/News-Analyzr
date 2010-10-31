from django.contrib         import admin
from organizations.models   import *

class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    pass

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'homepage', 'organization_type', 'modified']
    search_fields = ['name']
    pass
    
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    pass

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'homepage', 'organization', 'product_type']
    search_fields = ['name', 'product_type']
    pass

admin.site.register(OrganizationType, OrganizationTypeAdmin)    
admin.site.register(Organization, OrganizationAdmin)    
    
admin.site.register(ProductType, ProductTypeAdmin)    
admin.site.register(Product, ProductAdmin)