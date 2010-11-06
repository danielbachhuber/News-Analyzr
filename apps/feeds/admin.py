from django.contrib         import admin
from apps.feeds.models      import *

class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'modified']
    search_fields = ['title', 'url']
    pass

admin.site.register(Feed, FeedAdmin)