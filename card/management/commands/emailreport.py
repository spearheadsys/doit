from django.core.management.base import BaseCommand
from card.models import Card
from django.contrib.auth.models import User
# from datetime import date, datetime
import datetime
from django.core.mail import send_mail
import operator
import pprint
# testing html email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
# testing html email
from django.conf import settings

doit_myemail = settings.DOIT_MYEMAIL
today_date = datetime.datetime.now()
today_date = today_date.replace(hour=0, minute=0, second=0, microsecond=0)


# TODO:
class Command(BaseCommand):
    help = "Shows which cards are expiring today and a listing of \
        overdue cards."

    def add_arguments(self, parser):
        parser.add_argument('period', nargs="+", type=int)

    def handle(self, *args, **options):
        # TODO: add help text
        # TODO case period (day, week, month, year)
        period = options['period']


# NEW SENDING
plaintext = get_template('cards/emails/daily.txt')
html = get_template('cards/emails/daily.html')

users = User.objects.all().filter(is_staff=True, is_active=True)
# users = User.objects.filter(username="mariusp")
cardlist = {}
overduelist = {}
duetoday = {}
# TODO: get all cards but those in waiting and done columns
for user in users:
    # clear the dictionaries
    cardlist.clear()
    overduelist.clear()
    duetoday.clear()
    # get all cards assigned per user
    # TODO: look up notif preferences once we have such prefs :)
    cards = Card.objects.all().filter(owner=user)
    for card in cards:
        if not card.is_done and card.owner == user:
            # print card.title, card.is_done, card.due_date, card.owner
            cardlist[int(card.id)] = (card.title,
                                      card.due_date,
                                      card.owner)

    for (k) in cardlist:
        card = Card.objects.get(id=k)
        if card.is_overdue:
            overduelist[int(card.id)] = (
                card.title,
                card.due_date,
                card.owner)

    sorted_cards = sorted(cardlist.items(), key=operator.itemgetter(1))
    for (k, v) in sorted_cards:
        if v[1] and v[1] >= today_date:
            duetoday[int(card.id)] = (
                card.title,
                card.due_date,
                card.owner)

    # print(" what the >>>> ", overduelist)

    d = Context({
        'username': user.username,
        'cardlist': cardlist,
        'overduecards': overduelist,
        'duetoday': int(len(duetoday.keys())),
    })

    # print("email >>> ", user.email)

    subject, from_email, to = 'DoIT Daily Cards Report', doit_myemail, [str(user.email)]
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
# END NEW SENDING
