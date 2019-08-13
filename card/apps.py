from django.apps import AppConfig

#print "in the apps.py >>>>>>>>>>>>>>>>>>>>>>>>>>>>"


class CardConfig(AppConfig):
	name = 'card'
	verbose_name = 'DoIT Card'

	def ready(self):
		# import signal handlers
		import card.signals.signals