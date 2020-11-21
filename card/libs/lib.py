#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from card.models import Card, Board
from contact.models import UserProfile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import pytz
from django.template.loader import get_template
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

doit_myemail = settings.DOIT_MYEMAIL
doit_email_subject_keyword = settings.DOIT_EMAIL_SUBJECT_KEYWORD


def convert_to_localtime(uid, utctime):
    fmt = '%d/%m/%Y %H:%M'
    user_timezone = UserProfile.objects.filter(id=uid)
    utc = utctime.replace(tzinfo=pytz.UTC)
    local = utc.astimezone(user_timezone.timezone)
    return local.strftime(fmt)


def sendmail_card_created(cardid, card_creator):
    html_template = get_template('cards/emails/card_created.html')
    text_template = get_template('cards/emails/card_created.txt')
    if cardid:
        card = Card.objects.get(id=cardid)
        content = {
            'card': card
        }
        # todo: try to clean this up (not sure about the catch/except)
        try:
            subject = "DoIT "+doit_email_subject_keyword+"{} {}".format(card.id, card.title)
            from_email, to = doit_myemail, card.owner.email
            text_content = text_template.render(content)
            html_content = html_template.render(content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.mixed_subtype = 'related'
            msg.send()
        except AttributeError:
            pass


def sendmail_card_updated(cardid, comment):
    if cardid and comment.comment:
        card = Card.objects.get(id=cardid)
        subject = "DoIT " + doit_email_subject_keyword + "{} {}".format(card.id, card.title)
        watchers = card.watchers.all()
        # strip out attachment
        # in the future we can inline them or add them as attachments
        bs = BeautifulSoup(comment.comment, "html.parser")
        soup = bs.find_all('figure')
        for figure in soup:
            if figure.img:
                figure.img.replace_with(
                    '<p style="text-decoration: underline">[ Attachment stripped. Login to DoIT to view. ]</p>')
            # else:
            # todo: do we need to do anything here?
            # attachment was not of type image
            # figure["data-trix-attachment"]
            # print(ast.literal_eval(figure.attrs["data-trix-attachment"])['url'])

        html_template = get_template('cards/emails/card_updated.html')
        text_template = get_template('cards/emails/card_updated.txt')
        content = {
            'card': card,
            'comment': str(bs.contents[0])
        }
        text_content = text_template.render(content)
        html_content = html_template.render(content)
        # send to all watchers if public otherwise just operators and superusers
        for watcher in watchers:
            from_email, to = doit_myemail, watcher.email
            if comment.public:
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.mixed_subtype = 'related'
                msg.send()
            else:
                try:
                    account_type = User.objects.get(email=watcher)
                    if account_type.is_superuser or account_type.is_operator:
                        # text_content = text_template.render(content)
                        # html_content = html_template.render(content)
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.mixed_subtype = 'related'
                        msg.send()
                except:
                    pass

        # send to owner
        try:
            from_email, to = doit_myemail, card.owner.email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.mixed_subtype = 'related'
            msg.send()
        except AttributeError:
            pass


def doit_tracker(objid):
    # print 'we got an id >>>'
    pass


def org_stats(org):
    open_cards = Card.objects.all().filter(company=org, closed=False)
    closed_cards = Card.objects.all().filter(company=org, closed=True)
    open_boards = Board.objects.all().filter(archived=False)
    archived_boards = Board.objects.all().filter(archived=True)

    org_stats = {}
    # print open_cards.count()

    org_card_stats = open_cards | closed_cards

    # this works in views
    #closed_cards = lib.org_stats(up.company).filter(closed=True)

    return org_card_stats


def operator_stats():
    operators = UserProfile.objects.all().filter(is_operator=True)


def d_movecard(request, card, column, board=None):
    if request.is_ajax() or request.method == 'POST':
        card = request.POST['card']
        column = request.POST['column']
        # xhr = request.GET.has_key('xhr')
        previous_column = Card.objects.get(id=card).column
        # todo, if we were not moved ..
        # if int(column) ==  previous_column.id:
        workon_card = Card.objects.get(id=card)
        workon_card.column_id = column
        workon_card.modified_time = date.today()
        try:
            wcol = workon_card.column
        except AttributeError:
            wcol = None

        if str(wcol.usage) == "Done":
            workon_card.closed = True
            action_text = str(" closed the card ")
            workon_card.save()
        elif str(previous_column) == "Done" and str(wcol) == "Done":
            action_text = str(" updated already closed card ")
            workon_card.closed = True
            workon_card.save()
        elif str(previous_column) == "Done" and str(wcol) != "Done":
            action_text = str(" reopened closed card and placed it in the ") + str(wcol) + str(" column ")
            workon_card.closed = False
            workon_card.save()
        else:
            action_text=' from ' + str(previous_column) + ' to ' + str(workon_card.column)
            workon_card.save()

        # MOVE CREATED TRACKER
        ctype = ContentType.objects.get_for_model(workon_card)
        tracker = Tracker.objects.create(
            created_time=datetime.now(),
            content_type=ctype,
            object_id=workon_card.id,
            updated_fields=str(action_text),
            owner=request.user,
            action=str(" moved card "),
        )
        tracker.save()

        # END CARD CREATED TRACKER

        # TODO: remember this was stupid! It would redirect the ajax request
        # and return/reload the entire /cards (in this BoB) which slowed
        # things down considerably!!! stupid!
        # return HttpResponseRedirect("/cards/")
        return JsonResponse({'200': 'moved'})
    # print the form - nothing was submitted to POST
    else:
        # context = RequestContext(request)
        cards = Card.objects.all()
        columns = Column.objects.all()
        context_dict = {
            'site_title': "Cards | Spearhead Systems",
            'page_name': "Add Card",
            'columns': columns,
            'cards': cards, }
        # return render_to_response(
        #     'cards/movecard.html', context_dict, context)
        return render(request, 'cards/movecard.html', context_dict)