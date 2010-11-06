from django.contrib         import admin
from apps.products.models   import *

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    pass

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'homepage', 'organization', 'product_type']
    search_fields = ['name', 'product_type']
    pass   
    
admin.site.register(ProductType, ProductTypeAdmin)    
admin.site.register(Product, ProductAdmin)