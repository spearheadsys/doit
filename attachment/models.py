from django.db import models
from card.models import User, Card
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Attachment(models.Model):
    created_time = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User)
    content = models.FileField(upload_to='uploads')
    name = models.CharField(max_length=255)
    # TODO: automaitcally create this on save
    mimetype = models.CharField(max_length=255, null=True, blank=True)
    card = models.ForeignKey(Card, related_name="attachment_card")
    # # genericforeignkey kungfu
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.content.name
