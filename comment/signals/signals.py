# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from comment.models import Comment
# from datetime import datetime
# from django.contrib.contenttypes.models import ContentType
#
# @receiver(pre_save, sender=Comment)
# def comment_pre_save_signal(sender, instance, **kwargs):
#     print("COMMENT PRE SAVE SIGNAL >>>>>>")
#     obj = instance
#     old_object = Comment.objects.get(pk=obj.pk)
#     previous_column = old_object.column
#     current_column = obj.column
#     print(previous_column, current_column)