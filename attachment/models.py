from django.db import models
import os
from card.models import User
from organization.models import KnowledgeBaseArticle
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def get_upload_path(instance, filename):
    # path = 'uploads/{}/{}/{}'.format(related_card.board.id, related_card.id, uploaded_file)
    return os.path.join('uploads', "%d" % instance.card.id, "%d" % instance.card.board.id, "%s" % filename)


class Attachment(models.Model):
    created_time = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to=get_upload_path)
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255, null=True, blank=True)
    card = models.ForeignKey('card.Card', related_name="attachment_card", on_delete=models.CASCADE)

    def __str__(self):
        return self.content.name


# todo: implement post_delete.signal or similar to remove from filesystem
class KBAttachment(models.Model):
    created_time = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to=get_upload_path)
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255, null=True, blank=True)
    kbarticleid = models.ForeignKey(KnowledgeBaseArticle, related_name="attachment_kbarticle", on_delete=models.CASCADE)

    def __str__(self):
        return self.content.name