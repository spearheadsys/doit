from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Comments are public meaning the customers can see them
class Comment(models.Model):
    comment = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    public = models.BooleanField(default=False)

    # TODO: transfer worklogs to comments app so we can more easily post using
    # the reply mechanism in editcard
    minutes = models.IntegerField(blank=True, null=True)
    overtime = models.BooleanField(default=False)
    billable = models.BooleanField(default=True)

    # genericforeignkey kungfu
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.comment
