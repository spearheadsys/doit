from card.models import Card
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.mail import send_mail
import operator
from django.template import loader
from django.conf import settings

from board.models import Board

doit_myemail = settings.DOIT_MYEMAIL
today_date = datetime.datetime.now()
today_date = today_date.replace(hour=0, minute=0, second=0, microsecond=0)
seven_days_from_now = datetime.now() + timedelta(days=7)


# todo. prameterize this: date/range, user, watchers, etc.
# def get_overdue_cards():
# 	overdue_in_seven = Card.objects.filter(due_date__gte=datetime.now(), due_date__lte=seven_days_from_now).filter(
# 		closed=False).order_by('due_date').filter(owner=request.user)


def generate_card_stats(period, user):
    # period = period
    # user = user
    users = User.objects.all().filter(is_staff=True)

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

        # message text format
        message = """
Hi %s,

Here is your DoIT daily Cards report.

All your Cards: %d
Overdue Cards: %d
Cards due today: %d
"""

        overduecardlist = {}
        overduecardlist.clear()
        for i in overduelist:
            card = Card.objects.get(id=i)
            overduecardlist[i] = (str(card.title).encode('utf-8'),
                                  str(card.company.name).encode('utf-8'),
                                  str(card.priority).encode('utf-8'),
                                  str(card.due_date).encode('utf-8')
                                  )

        # gigi = pprint(overduecardlist, indent=2)
        message += """

Here is a list of your overdue cards:
%s

"""

        message += """

--
Spearhead Systems
DoIT

"""

        # message in html format
        #  testing
        html_message = loader.render_to_string(
            'doit/card_stats_email.html',
            {

            }
        )

        formatted_message = message % (
            str(user.first_name + " " + user.last_name),
            int(len(cardlist.keys())),
            int(len(overduelist.keys())),
            int(len(duetoday.keys())),
            # pprint.pformat(overduecardlist, indent=4),
        )
        # changed and prepare appropriate message
        send_mail(
            'DoIT daily Cards report',
            formatted_message,
            doit_myemail,
            [str(user.email)],
            fail_silently=False, html_message=html_message)


def board_per_user(user):
    all_boards = Board.objects.all().filter(owner=user)
    return all_boards