from django.core.management.base import BaseCommand
from card.models import Card, Reminder
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

doit_myemail = settings.DOIT_MYEMAIL
seven_days_from_now = datetime.now() + timedelta(days=7)
past_seven_days = datetime.now() - timedelta(days=7)
today_date = datetime.now()

# We send overdue reminders ONLY to owners!
# We work only on UTC times here!


class Command(BaseCommand):
    help = 'Sends reminders and notifications. This usually runs via CRON.'

    def add_arguments(self, parser):
        parser.add_argument('--reminders', action="store_true", help='Send user-defined Card reminders to owners (only).')
        parser.add_argument('--waiting', action="store_true", help='Send waiting for more than 48 \
            hours notifications to owners (only).')
        parser.add_argument('--overdue', action="store_true", help='Send overdue notifications to owners (only). \
            This is sent usually at the beginning of the day to point out overdue Cards.')
        parser.add_argument('--weeklydashboardreport', action="store_true", help='Weekly Dashboard Report.')

    def handle(self, *args, **options):
        if options['reminders']:
            print("WORKING ON reminders")
            reminders = Reminder.objects.all().filter(notified=False).filter()
            for i in reminders:
                print("LOOPING through reminders!")
                now = timezone.now()
                print("REMINDER - NOW - REMINDER TIME")
                print(i.card.id, now.strftime("%Y-%m-%d %H:%M"), i.reminder_time.strftime("%Y-%m-%d %H:%M"))
                if i.card.closed:
                    break

                if i.reminder_time.strftime("%Y-%m-%d %H:%M") == now.strftime("%Y-%m-%d %H:%M"):
                    plaintext = get_template('emails/reminder.txt')
                    html = get_template('emails/reminder.html')
                    d = {
                            'card': i.card
                        }
                    subject, from_email, to = 'DoIT Reminder', doit_myemail, [
                        str(i.card.owner.email)]
                    text_content = plaintext.render(d)
                    html_content = html.render(d)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    i.notified = True
                    i.save()
        elif options['overdue']:
            all_cards = Card.objects.all().filter(closed=False)
            overdue_cards = []
            for card in all_cards:
                if str(card.column.usage) != "Backlog":
                    if card.is_overdue:
                        overdue_cards.append(card)

            for user in User.objects.all().filter(is_active=True):
                try:
                    if user.profile_user.is_operator and user.email:
                        overdue_cards_per_user = [c for c in overdue_cards if c.owner == user]
                        if overdue_cards_per_user:
                            plaintext = get_template('emails/overdue.txt')
                            d = {
                                'owner': user,
                                'overdue_cards': overdue_cards_per_user,
                            }
                            subject, from_email, to = 'DoIT Overdue Cards', doit_myemail, [user.email]
                            text_content = plaintext.render(d)
                            # html_content = html.render(d)
                            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                            # msg.attach_alternative(html_content, "text/html")
                            msg.send()
                except:
                    # TODO: ugly, make it not so
                    pass
        elif options['waiting']:
            print("we're doing waiting")
            exit()
        elif options['weeklydashboardreport']:
            # what templates are we using
            plaintext = get_template('emails/weeklydashboardreport.txt')
            html = get_template('emails/weeklydashboardreport.html')
            # TODO: we're temporarily using is_Staff to differentiate between operators and customers (potential watchers)
            users = User.objects.all().filter(is_active=True, is_staff=True)
            for u in users:
                # todo: check at some point if they want these notificatins (opt-in/out)
                overdueCards = Card.objects.filter(due_date__lt=today_date).filter(closed=False).filter(owner=u).count()
                overdue_in_seven = Card.objects.filter(due_date__gte=today_date,due_date__lte=seven_days_from_now).filter(closed=False).order_by('due_date').filter(owner=u).count
                closed = Card.objects.filter(closed=True).filter(
                    modified_time__range=[past_seven_days, today_date]).filter(owner=u).count()

                d = Context(
                    {
                        'overdueCards': overdueCards,
                        'overdue_in_seven': overdue_in_seven,
                        'closed': closed,
                     }
                )

                subject, from_email, to = 'DoIT Weekly Dashboard Report', doit_myemail, [
                    str(u.email)]
                text_content = plaintext.render(d)
                html_content = html.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        else:
            print("we were called without any arguments. choose something")
            exit()

        # This should not be necessary for others. It loops through all cards
        # that were closed before the closed attribute was added to card.models
        # and therefore we had to close them 'manually'.
        # Before running make sure your columns usage is correct (card.e. done is Done)
        # for card in cards:
        #     if str(card.column.usage) == "Done":
        #         print("card %s is not closed, in column %s.") % (card.id, card.column)
        #         card.closed = True
        #         card.save()

        # for card in cards:
        #     print("card %s is not closed, in column %s. on board %s") % (card.id, card.column, card.board)


