from django.contrib         import admin
from apps.facebook.models   import *

class FacebookPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'modified']
    search_fields = ['name']
    pass

admin.site.register(FacebookPage, FacebookPageAdmin)