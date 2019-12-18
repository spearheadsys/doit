from django.db import models
import os
from card.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def get_upload_path(instance, filename):
    print("UPLOAD_PATH >>> ", instance, filename)
    return os.path.join(
        "%d" % instance.id, "%s" % instance.slug, filename)

# Create your models here.
class Attachment(models.Model):
    created_time = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User)
    content = models.FileField(upload_to=get_upload_path)
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255, null=True, blank=True)
    card = models.ForeignKey('card.Card', related_name="attachment_card")

    def __unicode__(self):
        return self.content.name
