from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# TODO : add gamification such as
# ticket closed in less than 60 minutes
# 10 tickets closed in a day
# 5 tickets closed in a day

# get some more ideas in here


class Tracker(models.Model):
    owner = models.ForeignKey(User, null=False, blank=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    # actions are usually the view name...
    # look for # TRACKER start/end comments
    action = models.CharField(max_length=150, blank=True, null=True)
    updated_fields = models.TextField()
    ordering =  ordering = ['-created_time']
