# from django.db.models.signals import post_save, pre_save, post_init
# from django.dispatch import receiver
# from card.models import Card, Worklog
# from doit.models import Tracker
# from datetime import datetime
# from django.contrib.contenttypes.models import ContentType


# @receiver(post_save, sender=Card)
# def card_created_signal(sender, instance, **kwargs):
# 	#print kwargs
# 	the_worklog = Worklog.objects.get(pk=instance.pk)
# 	if kwargs.get('created', False):
# 		#ctype = ContentType.objects.get_for_model(card_object)
# 		# taskg_obj = Task.objects.create(
# 		# 	task=task,
# 		# 	content_type=ctype,
# 		# 	object_id=card_object.id,
# 		# 	owner=userid
# 		# )
# 		ctype = ContentType.objects.get_for_model(the_worklog)
# 		updates = {
# 			'description': the_worklog.description,
# 			'minutes': the_worklog.minutes,
# 			'billable': the_worklog.billable,
# 			'overtime': the_worklog.overtime
# 		}
#
# 		tracker = Tracker.objects.create(
# 			created_time=datetime.now(),
# 			content_type=ctype,
# 			object_id=the_worklog.id,
# 			updated_fields=updates,
# 			owner=the_worklog.owner
# 		)
# 		tracker.save()

#
# @receiver(post_save, sender=Card)
# def card_post_created_signal(instance, **kwargs):
#     # print kwargs
#     # print "CARD_POST_CREATED_SIGNAL >>>>>>>>>>>>>> "
#     the_card = Card.objects.get(pk=instance.pk)
#     if the_card.closed:
#         print("SIGNAL >>>>> The card %s is in state %s ") % (the_card.title, str(the_card.closed))
#     else:
#         print("SIGNAL >>>>> This card is not closed.")
#     if kwargs.get('created', False):
#         print("SIGNAL >>>>> This card is closed.")



    # tracker = Tracker.objects.create(
    # 	created_time=datetime.now(),
    # 	content_type=ctype,
    # 	object_id=the_card.id,
    # 	updated_fields=updates,
    # 	owner=the_card.owner
    # )
    # tracker.save()

# @receiver(post_save, sender=Card, dispatch_uid="Card.Post.Save.Signal")
# def card_post_created_signal(sender, instance, created, **kwargs):
# the_card = Card.objects.get(pk=instance.pk)
# if 'created' in kwargs:
# 	if kwargs['created']:
# 		created=True
# 	print "true"
# else:
# 	print "false"

# print created
# print "<<<<<< separator >>>>>>>>>>"
# if created:
# 	print "true >>>>>>>>>"


# if kwargs.get('created'):

# it means we're updating a new instance
# else:
# were dealing with a new card
# print "false >>>>>>>>>"

# ctype = ContentType.objects.get_for_model(card_object)
# taskg_obj = Task.objects.create(
# 	task=task,
# 	content_type=ctype,
# 	object_id=card_object.id,
# 	owner=userid
# )
# ctype = ContentType.objects.get_for_model(the_worklog)
# updates = {}
# # TODO: not happy hardcondig this here
# updates['description'] = the_worklog.description
# updates['minutes'] = the_worklog.minutes
# updates['billable'] = the_worklog.billable
# updates['overtime'] = the_worklog.overtime

# maybe we can automate by doing this but how then do we
# exclude what is not of interest?
# for name in Worklog._meta.get_all_field_names():
# 	updates[name] = the_worklog.

# tracker = Tracker.objects.create(
# 	created_time=datetime.now(),
# 	content_type=ctype,
# 	object_id=the_worklog.id,
# 	updated_fields=updates,
# 	owner=the_worklog.owner
# )
# tracker.save()

# @receiver(pre_init, sender=Card)
# def card_pre_init_signal(sender, **kwargs):
# 	print "PRE INIT SIGNAL >>>>>>"
# 	print kwargs
# 	print sender


# @receiver(post_init, sender=Card, dispatch_uid="card_pre_save_disp_uid")
# def card_post_init_created_signal(instance, **kwargs):
#     obj = instance
#     old_object = Card.objects.get(pk=obj.pk)
#     previous_column = old_object.column
#     current_column = obj.column
#     print(previous_column, current_column)




# @receiver(pre_save, sender=Card, dispatch_uid="card_pre_save_disp_uid")
# def card_pre_save_signal(sender, instance, **kwargs):
#     obj = instance
#     old_object = Card.objects.get(pk=obj.pk)
#     previous_column = old_object.column
#     current_column = obj.column
#     print(previous_column, current_column)


# @receiver(post_save, sender=Card, dispatch_uid="card_post_save_disp_uid")
# def card_post_created_signal(instance, created, **kwargs):
#     print("CARD POST SAVE SIGNAL >>>>>>>")
#     obj = instance
#     old_object = Card.objects.get(pk=obj.pk)
#     previous_column = old_object.column
#     current_column = obj.column
#     print(previous_column, current_column)

# signals.post_save.connect(card_created_signal, sender=Card)
