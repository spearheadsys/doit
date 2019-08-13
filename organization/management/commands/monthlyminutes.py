from django.core.management.base import BaseCommand, CommandError
from card.models import Worklog
from organization.models import Organization
import django.core.exceptions
from datetime import datetime, date, timedelta
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings

doit_myemail = settings.DOIT_MYEMAIL
today_date = date.today()

# TODO:
# we're hardconding the minutes here but it could be set on the organization
# model
class Command(BaseCommand):
	help = 'Checks a boards mailbox, fetches and processes new emails.'

	def add_arguments(self, parser):
		parser.add_argument('organization_id', nargs="+", type=int)

	def handle(self, *args, **options):
		organizationid = options['organization_id']
		organization = Organization.objects.get(id=organizationid[0])
		worklogs = Worklog.objects.all().filter(
			created_time__month=today_date.month,
			card__company_id=organizationid[0]
		)


		minutesthismonth = worklogs.aggregate(Sum("minutes"))
		#print type(minutesthismonth["minutes__sum"])
		limit = int(2160)

		if minutesthismonth["minutes__sum"] > limit:
			print "Minutes for company %s : %d" % (
				organization.name, minutesthismonth["minutes__sum"])

			message = """
Workflow for time worked has been triggered.

Details:
	Organization: %s
	Minutes: %d

--
Spearhead Systems
DoIT

"""

			formatted_message = message % (
				organization.name,
				minutesthismonth["minutes__sum"])
			# changed and prepare appropriate message
			send_mail(
				'DoIT time worked workflow: ' + organization.name,
				formatted_message,
				doit_myemail,
				['marius.pana@sphs.ro'],
				fail_silently=False)
