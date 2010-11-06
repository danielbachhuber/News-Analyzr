from django.contrib         import admin
from apps.twitter.models   import *

class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'twitter_id', 'modified']
    search_fields = ['username']
    pass

admin.site.register(TwitterAccount, TwitterAccountAdmin)