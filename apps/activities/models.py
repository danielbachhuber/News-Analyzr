from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Activity(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.TextField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    # user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=True)

def save_activity(sender, instance, created, **kwargs):
    if sender._meta.app_label == 'organizations':
        activity = Activity()
        activity.content_type = ContentType.objects.get_for_model(sender)
        activity.object_id = instance.pk
        activity.save()
models.signals.post_save.connect(save_activity)