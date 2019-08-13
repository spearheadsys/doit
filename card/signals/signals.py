from django.db.models.signals import post_save
from django.dispatch import receiver
from card.models import Card, Worklog
from doit.models import Tracker
from datetime import datetime
from django.contrib.contenttypes.models import ContentType


# @receiver(post_save, sender=Worklog)
# def worklog_post_created_signal(sender, instance, **kwargs):
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
@receiver(post_save, sender=Card)
def card_post_created_signal(instance, **kwargs):
    # print kwargs
    # print "CARD_POST_CREATED_SIGNAL >>>>>>>>>>>>>> "
    the_card = Card.objects.get(pk=instance.pk)
    if the_card.closed:
        print("The card %s is in state %s ") % (the_card.title, str(the_card.closed))
    else:
        print("This card is not closed.")
    if kwargs.get('created', False):
        print("This card is closed.")



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


# @receiver(post_init, sender=Card)
# def card_post_init_created_signal(instance, create, **kwargs):
# 	print "POST INIT SIGNAL >>>>>>"
# 	print kwargs


# @receiver(pre_save, sender=Card)
# def card_pre_created_signal(**kwargs):
# 	print "PRE SAVE SIGNAL >>>>>>"
# 	print kwargs


# @receiver(post_save, sender=Card)
# def card_post_created_signal(instance, created, **kwargs):
# 	print "POST SAVE SIGNAL >>>>>>>"
# 	print kwargs

# 	if created:
# 		obj = instance
# 		# get owners email
# 		# we should do this some other way
# 		try:
# 			owner_email = obj.owner.email
# 		except:
# 			None
# 			# sys.exit(0)
# 			# watchers =
# 		message = """
# 			A new card has been Created.
#
# 			Details:
# 				Card title: %s
# 				Assigned to: %s
# 				Description: %s
# 				Priority: %s
#
# 			For more details view http://doit.sphs.ro.
#
# 			--
# 			You received this message because you are either the owner or a
# 			watcher for this card.
#
# 			You can modify your email preferences <a href="#">here</a>.
# 			"""
# 		formatted_message = message % (obj.title, obj.owner, obj.description, obj.priority)
# 		# todo: add to eventual tracker
# 		# todo check via if or something whether something changed, what
# 		# changed and prepare appropriate message
# 		send_mail(
# 			'DoIT card created: ' + obj.title,
# 			formatted_message, 'doit@sphs.ro',
# 			[owner_email],
# 			fail_silently=False)
# 	else:
# 		print ">>>>> card_UPDATED_signal >>>>>"
# 		obj = instance
# 		old_object = Card.objects.get(pk=obj.pk)
# 		cardid = old_object.id
# 		# 	# get owners email
# 		# I believe this is ugly and we should do this some other way
# 		try:
# 			owner_email = obj.owner.email
# 		except:
# 			# pass - portal users do not assign an owner
# 			pass
# 			# sys.exit(0)
# 		# 	# todo: get watchers of card to set-up recipients list
# 		# 	# todo: if owner change do something special
# 		previous_column = old_object.column
# 		current_column = obj.column
# 		message = """
# The Card with id (%s) has been updated.
#
# For more details view click here.
#
# --
# You received this message because you are either the owner or a watcher for this card.
# You can modify your email preferences here.
# """
# 		formatted_message = message % cardid
# 		# 	#todo: add to eventual tracker
# 		# 	#todo check via if or something whether something changed,
# 		# what changed and prepare appropriate message
# 		send_mail(
# 			'DoIT card modified: ' + obj.title,
# 			formatted_message, 'doit@sphs.ro',
# 			[owner_email],
# 			fail_silently=False)
#
# signals.post_save.connect(card_created_signal, sender=Card)
