# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import resolve
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render
# user auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
# json and serializer
import json
from django.core import serializers
# helps us negate objects
from django.db.models import Q, Sum, Max, Min, F
# doit models
from card.models import Card, Column, Organization, Board, Columntype
from comment.models import Comment
from contact.models import UserProfile
from attachment.models import Attachment
from attachment.forms import AttachmentForm
from comment.forms import CommentForm
# forms
from card.forms import CardsForm, ColumnForm, EditCardForm, \
    EditColumnForm, BoardFormSet
# date stuff
from datetime import date, datetime, timedelta, timezone
from django.views.decorators.csrf import csrf_exempt
# django settings
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from doit.models import Tracker
import simplejson
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dal import autocomplete
from taggit.models import Tag
# calendar
from django.utils.safestring import mark_safe
from django.utils import timezone
# import our card libs
from card.libs import lib
from card.cardcalendar import CardCalendar
from email.utils import parseaddr, getaddresses
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
import re
import ast

# GLOBALS
doitVersion = settings.DOIT_VERSION
doit_myemail = settings.DOIT_MYEMAIL
SITE_URL = settings.SITE_URL
doit_default_board = settings.DOIT_DEFAULT_BOARD
doit_email_subject_keyword = settings.DOIT_EMAIL_SUBJECT_KEYWORD

@login_required
@staff_member_required
def cards(request):
    # get the board we're working on
    if request.GET.get('board'):
        board_id = request.GET['board']

        # TODO: standard stuff for all views

    else:
        #  no board ID means BoB as of 15.04.2016
        columnDone = Columntype.objects.all().filter(name="Done")
        cards = Card.objects.all().filter(
            ~Q(column__usage=columnDone),
        ).order_by('order')

        context = RequestContext(request)
        context_dict = {
            'site_title': "Cards | Spearhead Systems",
            'page_name': "BoB",
            'cards': cards,
            'doitVersion': doitVersion,
        }
        return render(request, 'boards/bob.html', context_dict)

    boards = Board.objects.filter(archived=False)

    # closed cards - in done column (attempted pagination fail)
    if request.user.profile_user.is_operator:
        numbers_list = Card.objects.all().filter(board=board_id).filter(closed=True).order_by('order')[:10]
        page = request.GET.get('page', 1)
        paginator = Paginator(numbers_list, 10)
        try:
            numbers = paginator.page(page)
        except PageNotAnInteger:
            numbers = paginator.page(1)
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)

        boardname = Board.objects.get(id=board_id)
        columns = Column.objects.filter(board=board_id).order_by('order')
        u = User.objects.get(username=request.user)
        done_order = \
            Column.objects.all().filter(
                board=board_id).select_related().aggregate(
                Max('order'))['order__max']
        done_column = Column.objects.filter(board=board_id, order=done_order)
        # get assigned and overdue card per board for the status bar
        today_date = date.today()
        all_cards_but_deleted = Card.objects.all().filter(closed=False).filter(board=board_id).order_by('order')

        first_column = \
            Column.objects.all().filter(board=board_id).select_related().aggregate(
                Min('id'))['id__min']
        # addcard form for modal
        addCardForm = CardsForm(
            initial={
                # 'owner': u.id,
                'board': board_id,
                'column': first_column,
                'priority': '1',
            },
            board_id=board_id
        )
        addCardForm.fields['watchers'].queryset = User.objects.filter(is_active=True)
        editColumnForm = EditColumnForm()
        cardslist = list(all_cards_but_deleted)
        cards = cardslist
        # cards = sorted(cardslist,key=lambda x: str(x))
    else:
        u = User.objects.get(username=request.user)
        up = UserProfile.objects.get(user=u)
        # check for user as owner or watcher/contact on board
        board = Board.objects.get(id=board_id)
        if u.id != board.owner.id:
            return HttpResponse("You do not have permissions to view this page.")

        # end check user perms

        numbers_list = Card.objects.filter(board=board_id).filter(closed=True).filter(owner=request.user).order_by('order')[:10]
        page = request.GET.get('page', 1)
        paginator = Paginator(numbers_list, 10)
        try:
            numbers = paginator.page(page)
        except PageNotAnInteger:
            numbers = paginator.page(1)
        except EmptyPage:
            numbers = paginator.page(paginator.num_pages)

        boardname = Board.objects.get(id=board_id)
        columns = Column.objects.filter(board=board_id).order_by('order')

        done_order = \
            Column.objects.all().filter(
                board=board_id).select_related().aggregate(
                Max('order'))['order__max']
        done_column = Column.objects.filter(board=board_id, order=done_order)
        today_date = date.today()
        # all_cards_but_deleted = Card.objects.select_related().filter(
        #     ~Q(column_id=done_column),
        #     Q(board=board_id),
        # ).filter(owner=u)
        all_cards_but_deleted = Card.objects.select_related().filter(closed=False).filter(board=board_id).filter(owner=u).order_by('order')
        gg = Card.objects.filter(closed=False).filter(watchers__id__exact=request.user.id).order_by('order')
        new_cards_list = list(all_cards_but_deleted) + list(gg)
        first_column = \
            Column.objects.all().filter(board=board_id).select_related().aggregate(
                Min('id'))['id__min']
        addCardForm = CardsForm(
            initial={
                # 'owner': u.id,
                'board': board_id,
                'column': first_column,
                'priority': '1',
            },
            board_id=board_id
        )
        addCardForm.fields['watchers'].queryset = User.objects.filter(is_active=True)
        editColumnForm = EditColumnForm()
        cardslist = list(new_cards_list)
        cards = sorted(cardslist,key=lambda x: str(x))

    context = RequestContext(request)
    context_dict = {
        'site_title': "Cards | Spearhead Systems",
        'page_name': "Cards",
        'cards': cards,
        'columns': columns,
        'addCardForm': addCardForm,
        'editColumnForm': editColumnForm,
        'boardname': boardname,
        'doitVersion': doitVersion,
        'year': today_date.year,
        'month': today_date.month,
        'numbers': numbers,
        'boards': boards,
    }

    return render(request, 'cards/cards.html', context_dict)


@login_required
@staff_member_required
def calendar(request, year=2017, month=1):
    my_cards = Card.objects.order_by('due_date').filter(
        due_date__year=year, due_date__month=month
    )
    cal = CardCalendar(my_cards).formatmonth(year, month)
    # return render_to_response(
    #     'cards/calendar.html',
    #     {'calendar': mark_safe(cal), }
    # )
    return render(request, 'cards/calendar.html', {'calendar': mark_safe(cal), })



# tags for autocomplete
class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


# watchers for autocomplete
class WatcherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = User.objects.all().filter(is_active=True).order_by('username')

        if self.q:
             qs = qs.filter(username__icontains=self.q)

        return qs


# company for autocomplete
class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return None

        qs = Organization.objects.all().filter(active=True).order_by('name')

        if self.q:
             qs = qs.filter(name__icontains=self.q)

        return qs


# owner for autocomplete
class OwnerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = User.objects.all().filter(is_active=True).filter(profile_user__is_operator=True).order_by('username')

        if self.q:
             qs = qs.filter(username__icontains=self.q)

        return qs


@login_required
# @staff_member_required
# TODO: this does not bode well. Figure out why nginx/gunicorn
# complain about csrf
@csrf_exempt
def addcard(request):
    u = User.objects.get(username=request.user)
    # If the form has been submitted...

    if request.is_ajax() or request.method == 'POST':
        card_title = request.POST['title']
        card_column = request.POST['column']
        card_description = request.POST['description']
        card_priority = request.POST['priority']
        card_due_date = request.POST.get('due_date', None)
        if not card_due_date:
            card_due_date = None
        card_start_time = request.POST.get('start_time', None)
        if not card_start_time:
            card_start_time = None
        card_tags = request.POST.getlist('tags')
        card_company = request.POST.get('company')
        card_board = request.POST.get('board')
        card_owner = request.POST.get('owner', None)
        card_watchers = request.POST.getlist('watchers')
        if not card_watchers:
            # are we a customer?
            if u.profile_user.is_customer:
                card_watchers.append(u.id)
        card_type = request.POST.get('type')
        card_estimate = request.POST.get('estimate', 0)


        # if not card_owner and request.user.profile_user.is_customer:
        #     card_owner = None
        # else:
        #     card_owner = u.id

        if not request.user.profile_user.is_customer:
            card_created = Card.objects.create(
                owner_id=card_owner,
                created_by_id=u.id,
                board_id=card_board,
                priority_id=card_priority,
                company_id=card_company,
                column_id=card_column,
                title=card_title,
                description=card_description,
                due_date=card_due_date,
                start_time=card_start_time,
                type=card_type,
                estimate=card_estimate,
                csat=0)
        else:
            card_created = Card.objects.create(
                created_by_id=u.id,
                board_id=card_board,
                priority_id=card_priority,
                company_id=card_company,
                column_id=card_column,
                title=card_title,
                description=card_description,
                due_date=card_due_date,
                start_time=card_start_time,
                type=card_type,
                estimate=card_estimate,
                csat=0)


        # we should add the card to the end of the list not the top
        # Column.objects.all().filter(
        #   board=board_id).select_related().aggregate(
        #   Max('order'))['order__max']
        # TODO: maybe we can do it some other way? something more efficient
        highiest = Card.objects.all().aggregate(Max('order'))['order__max']
        card_created.order = highiest
        card_created.save()
        # now we can save the m2m relations to watchers
        for w in card_watchers:
            d = User.objects.get(id=w)
            d.Watchers.add(card_created)
            d.save()
        # save the tags
        for t in card_tags:
            card_created.tags.add(t)
        # CARD CREATED TRACKER
        ctype = ContentType.objects.get_for_model(card_created)
        tracker = Tracker.objects.create(
            created_time=datetime.now(),
            content_type=ctype,
            object_id=card_created.id,
            action=[card_created.board.id, card_created.column.id],
            updated_fields="created ['card']",
            owner=u,
        )
        tracker.save()
        # END CARD CREATED TRACKER
        # my libs
        # send notifications
        card_creator = request.user
        lib.sendmail_card_created(card_created.id, card_creator)
        redirect_url = "/cards/editcard/" + str(card_created.id)
        return HttpResponseRedirect(redirect_url)
    else:
        # we need to show the addcard form - based on user type

        # WTF? if no card owner is assigned we identify whether he is superuser or operator

        # if customer then we need to assign to organization owner
        if u.profile_user.is_customer:
            company = u.profile_user.company
            board = u.profile_user.company.default_board
            # how do we get the right column?
            # choose in the following order: queue, working
            default_org_board =  u.profile_user.company.default_board
            # TODO: every board MUST have a QUEUE type!
            column_type_usage = Columntype.objects.get(name="Queue")
            board_columns = Column.objects.filter(board=default_org_board.id)
            column = board_columns.get(usage=column_type_usage)
            # g = Board.objects.get(id=board.id)
            # org_owner = g.owner

            # we send to customer addcard form
            # addcardform = CardsForm(board_id=board, initial={'id_company:', company})
            addcardform = CardsForm(
                initial={
                    # 'owner': u.id,
                    'board': board.id,
                    'owner': None,
                    'column': column,
                    'company': company.id,
                    'priority': '1',
                    'estimate': 240,
                    'due_date': timezone.now()+timezone.timedelta(days=1),
                },
                board_id=board
            )
            context_dict = {
                'site_title': "Cards | Spearhead Systems",
                'page_name': "Add Card",
                'column': column.id,
                'owner': None,
                'company': company.id,
                'addcardform': addcardform,
                'board': Board.objects.get(id=board.id),
                'boards': Board.objects.filter(archived=False)
            }
            return render(request, 'cards/addcard-ext.html', context_dict)
        else:
            # display addcard page, get board id
            board = request.GET['board']
            company = request.GET['company']
            if 'column' in request.GET:
                column = request.GET['column']
            else:
                column = ''
            # addcardform = CardsForm(board_id=board, initial={'id_company:', company})
            addcardform = CardsForm(
                initial={
                    # 'owner': u.id,
                    'board': board,
                    'column': column,
                    'company': company,
                    'priority': '3',
                },
                board_id=board
            )
            # TODO: if we dont get a board id?
            if not addcardform:
               pass

            context_dict = {
                'site_title': "Cards | Spearhead Systems",
                'page_name': "Add Card",
                'addcardform': addcardform,
                'boards': Board.objects.filter(archived=False)
                # 'board': Board.objects.get(id=board)
            }
            return render(request, 'cards/addcard.html', context_dict)

@login_required
@staff_member_required
def addColumn(request):
    current_url = resolve(request.path_info).url_name

    if request.method == 'POST':
        form = ColumnForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cards/')

    context = RequestContext(request)
    formSet = BoardFormSet()
    form = ColumnForm()
    context_dict = {
        'site_title': "Cards | Spearhead Systems",
        'page_name': "Add a Column",
        'active_url': current_url,
        'form': form,
        'formSet': formSet, }
    return render(request, 'cards/addcolumn.html', context_dict, context)


@login_required
@staff_member_required
def deleteCard(request, card=None):
    """
    Delete a card.
    """
    if request.user.profile_user.is_superuser or request.user.profile_user.is_operator:
        # delete all attachments
        for a in Attachment.objects.filter(card=card):
            a.delete()
        # delete all comments
        for c in Comment.objects.filter(object_id=card):
            c.delete()
        # delete the card
        Card.objects.get(id=card).delete()
    # Todo: to where you came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
# @csrf_exempt # TODO: add csrf token
def movecard(request):
    # current_url = resolve(request.path_info).url_name
    if request.is_ajax() or request.method == 'POST':
        card = request.POST['card']
        column = request.POST['column']
        previous_column = Card.objects.get(id=card).column
        workon_card = Card.objects.get(id=card)
        workon_card.column_id = column
        workon_card.modified_time = date.today()
        try:
            wcol = workon_card.column
        except AttributeError:
            wcol = None

        card_trackers = Tracker.objects.filter(object_id=workon_card.id)
        last_tracker = card_trackers[card_trackers.count()-1]
        # print("last_tracker >>>> ", last_tracker.created_time)
        # if previous_column != "Backlog" or "Waiting":
            # print("calculate all working minutes since created_time to now")

        # print("last_tracker >>>> ", last_tracker.count())
        # print("last_tracker >>>> ", last_tracker[last_tracker.count()-1].created_time)

        if str(wcol.usage) == "Done":
            workon_card.closed = True
            action_text = " closed the card "
            updated_fields = "closed ['card']"
            # workon_card.save()
        elif str(previous_column) == "Done" and str(wcol) == "Done":
            action_text = str(" updated already closed card ")
            updated_fields = "updated ['card']"
            workon_card.closed = True
            # workon_card.save()
        elif str(previous_column) == "Done" and str(wcol) != "Done":
            action_text = str(" reopened closed card and placed it in the ") + str(wcol) + str(" column ")
            updated_fields = "updated ['card']"
            workon_card.closed = False
            # workon_card.save()
        else:
            action_text = [previous_column.id, workon_card.column.id]
            updated_fields = "updated ['card']"
        workon_card.save()

        # MOVE CREATED TRACKER
        ctype = ContentType.objects.get_for_model(workon_card)
        tracker = Tracker.objects.create(
            created_time=datetime.now(),
            content_type=ctype,
            object_id=workon_card.id,

            updated_fields=str("updated ['column']"),
            owner=request.user,
            action=action_text
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


@login_required
# @csrf_exempt # TODO: add csrf token
# def mergecard(request):
#     # current_url = resolve(request.path_info).url_name
#     if request.is_ajax() or request.method == 'POST':
#         card = request.POST['card']
#         column = request.POST['column']
#         previous_column = Card.objects.get(id=card).column
#         workon_card = Card.objects.get(id=card)
#         workon_card.column_id = column
#         workon_card.modified_time = date.today()
#         try:
#             wcol = workon_card.column
#         except AttributeError:
#             wcol = None
#
#         if str(wcol.usage) == "Done":
#             workon_card.closed = True
#             action_text = str(" closed the card ")
#             workon_card.save()
#         elif str(previous_column) == "Done" and str(wcol) == "Done":
#             action_text = str(" updated already closed card ")
#             workon_card.closed = True
#             workon_card.save()
#         elif str(previous_column) == "Done" and str(wcol) != "Done":
#             action_text = str(" reopened closed card and placed it in the ") + str(wcol) + str(" column ")
#             workon_card.closed = False
#             workon_card.save()
#         else:
#             action_text=' from ' + str(previous_column) + ' to ' + str(workon_card.column)
#             workon_card.save()
#
#         # MOVE CREATED TRACKER
#         ctype = ContentType.objects.get_for_model(workon_card)
#         tracker = Tracker.objects.create(
#             created_time=datetime.now(),
#             content_type=ctype,
#             object_id=workon_card.id,
#             updated_fields=str(action_text),
#             owner=request.user,
#             action=str(" moved card "),
#         )
#         tracker.save()
#
#         # END CARD CREATED TRACKER
#
#         # TODO: remember this was stupid! It would redirect the ajax request
#         # and return/reload the entire /cards (in this BoB) which slowed
#         # things down considerably!!! stupid!
#         # return HttpResponseRedirect("/cards/")
#         return JsonResponse({'200': 'moved'})
#     # print the form - nothing was submitted to POST
#     else:
#         # context = RequestContext(request)
#         cards = Card.objects.all()
#         columns = Column.objects.all()
#         context_dict = {
#             'site_title': "Cards | Spearhead Systems",
#             'page_name': "Add Card",
#             'columns': columns,
#             'cards': cards, }
#         # return render_to_response(
#         #     'cards/movecard.html', context_dict, context)
#         return render(request, 'cards/movecard.html', context_dict)


@login_required
def movecardtoboard(request):
    if request.is_ajax() or request.method == 'POST':
        card = request.POST['card']
        board = request.POST['board']
        column = request.POST['column']
        workon_card = Card.objects.get(id=card)
        workon_column = Column.objects.get(id=column)
        workon_board = Board.objects.get(id=board)
        new_column = Column.objects.get(id=column)
        previous_column = workon_card.column
        print(previous_column,new_column)
        if str(workon_column.usage) == "Done":
            workon_card.closed = True
            workon_card.column = new_column
            workon_card.board = workon_board
            action_text = str(" moved to board %s and closed the card ") % workon_board
            workon_card.save()
        elif str(previous_column) == "Done" and str(workon_column) == "Done":
            action_text = str(" updated already closed card from %s to %s ") % (workon_card.board, workon_board)
            workon_card.closed = True
            workon_card.column = new_column
            workon_card.board = workon_board
            workon_card.save()
        elif str(previous_column) == "Done" and str(workon_column) != "Done":
            action_text = str(" reopened closed card and placed it in the %s column on board %s") % \
                          (workon_column, workon_board)
            workon_card.closed = False
            workon_card.save()
        else:
            action_text = [previous_column.id, workon_column.id]
            workon_card.column = workon_column
            workon_card.board = workon_board
            workon_card.save()

        # MOVE CREATED TRACKER
        ctype = ContentType.objects.get_for_model(workon_card)
        tracker = Tracker.objects.create(
            created_time=datetime.now(),
            content_type=ctype,
            object_id=workon_card.id,
            updated_fields=str("moved card from board %s " % workon_board),
            owner=request.user,
            action=action_text
        )
        tracker.save()

        # END CARD MOVED TRACKER

        # refresh new editcard page with new details
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
@staff_member_required
@csrf_exempt # TODO: add csrf token
def update_card_order(request):
    """
    Update the order of a card within the list unless we are in a DONE column.
    """
    # current_url = resolve(request.path_info).url_name
    if request.is_ajax() or request.method == 'POST':
        card_order = request.POST.getlist('arr', False)
        order = json.loads(card_order[0])
        position = 0
        for card in order['elementsOrder']:
            card_obj = Card.objects.get(id=card)
            card_obj.order = position
            card_obj.save()
            position += 1
        # TODO: return something meaningul. maybe json
        # return render_to_response('cards/order.html')
        return render(request, 'cards/order.html')


@login_required
def closecard(request, card=None):
    card = Card.objects.get(id=card)
    done_column = Column.objects.all().filter(
        board=card.board.id).filter(usage__name="Done")
    # TODO: wtf, this needs cleaning
    context_dict = {
        'site_title': "Cards | Spearhead Systems",
        'page_name': "Close Card",
        'card': card,
    }
    # by looking at watchers, company with is_org_admin
    if request.user.profile_user.is_customer and \
            request.user.profile_user.is_org_admin:
        # check card company and watcher
        # if card in request.user.Watchers.all():
        #     print("we're in")
        card.column = done_column[0]
        card.closed = True
        card.save()
    else:
        return render(request, 'cards/closecardnok.html', context_dict)

    action_text = "card closed by customer"

    # closecard TRACKER
    ctype = ContentType.objects.get_for_model(card)
    tracker = Tracker.objects.create(
        created_time=datetime.now(),
        content_type=ctype,
        object_id=card.id,
        updated_fields=str(action_text),
        owner=request.user,
        action=str(" closed card "),
    )
    tracker.save()
    # END Cclosecard TRACKER

    context_dict = {
        'site_title': "Cards | Spearhead Systems",
        'page_name': "Close Card",
        'card': card,
    }
    return render(request, 'cards/closecard.html', context_dict)


@login_required
def reopencard(request, card=None):
    card = Card.objects.get(id=card)
    queue_column = Column.objects.all().filter(
        board=card.board.id).filter(usage__name="Queue")
    if not queue_column:
        return HttpResponse("We cannot reopen this Card for you without a Queue column! Please let \
            help@spearhead.systems now about this error.")
    # make sure user is part of card/warchers
    if request.user in card.watchers.all() or request.user.profile_user.company == card.company:
        print("request.user in card.watchers.all() >>>>")
        card.column = queue_column[0]
        card.closed = False
        card.save()
    else:
        return HttpResponse("Well now this is embarrassing :-/ ." \
                            "You do not seem to permissions to open this card." \
                            "Error code: DoIT-obj-ref: UP0001")

    action_text = "card reopend by customer"

    # reopen card TRACKER
    ctype = ContentType.objects.get_for_model(card)
    tracker = Tracker.objects.create(
        created_time=datetime.now(),
        content_type=ctype,
        object_id=card.id,
        updated_fields=str(action_text),
        owner=request.user,
        action=str(" reopened card "),
    )
    tracker.save()
    # END reopen card TRACKER

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def editCard(request, card=None):
    """
    Edit the properties of a Card.
    """
    instance = Card.objects.get(id=card)
    board = instance.board_id
    previous_column = Card.objects.get(id=card).column
    boards = Board.objects.filter(archived=False)

    if request.is_ajax() or request.method == 'POST':
        # TODO: post allowed only if in watcher, owner or superuser
        # if request.user.profile_user.is_customer and request.user in instance.watchers.all():
        #     pass
        form = EditCardForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # EDIT CARD TRACKER
            # TODO: get fields that were updated and show in history
            # eureka (changed_data att of forms!)
            if instance.company_id is None:
                company = ''
            if str(instance.column.usage) == "Done":
                instance.closed = True
                action_text = str(" closed the card ")
                instance.save()
            elif str(previous_column.usage) != "Done" and str(instance.column) == "Done":
                action_text = str(" closed the card ")
                instance.closed = True
                instance.save()
            elif str(previous_column.usage) == "Done" and str(instance.column) == "Done":
                action_text = str(" updated already closed card ")
                instance.closed = True
                instance.save()
            elif str(previous_column.usage) == "Done" and str(instance.column) != "Done":
                action_text = str(" reopened closed card and placed it in the ") + str(instance.column) + str(" column ")
                instance.closed = False
                instance.save()
            elif str(instance.column) != str(previous_column):
                action_text=[previous_column.id, instance.column.id]
            else:
                action_text=str(" edited the card ")
            ctype = ContentType.objects.get_for_model(instance)
            tracker = Tracker.objects.create(
                created_time=datetime.now(),
                content_type=ctype,
                object_id=instance.id,
                updated_fields=str("updated ") + str(form.changed_data),
                owner=request.user,
                action=action_text
            )
            tracker.save()
            # END EDIT CARD TRACKER
        else:
            context_dict = {
                'site_title': "Cards | Spearhead Systems",
                'page_name': "Edit Card",
                'card': card,
                'editcard_form': form,
                'boards': boards,
                'SITE_URL': SITE_URL,
            }
            return HttpResponse(form.errors)

        if request.is_ajax():
            return JsonResponse({'status': 'ok'})
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.user.profile_user.is_operator:
        card = Card.objects.select_related().get(id=card)
        # try:
        #     if card.company.sla_response_time is not None:
        #         print("BEFORE view sla_breached >>>", card.sla_breached())
        # except AttributeError:
        #     print("BEFORE no companu or sla", card.sla_breached())
        ctype = ContentType.objects.get_for_model(card)
        attachments = Attachment.objects.filter(
            card=card.id)
        comments = Comment.objects.filter(content_type__pk=ctype.id, object_id=card.id).order_by('-created_time')
        editcard_form = EditCardForm(instance=instance)
        editcard_form.fields['watchers'].queryset = User.objects.filter(is_active=True)
        editcard_form.fields['owner'].queryset = User.objects.filter(is_staff=True)
        # comments
        comment_form = CommentForm()
        card_watchers = User.objects.all().filter(Watchers=card.id)
        # get board id
        card_board = card.board_id
        editcard_form.fields["column"].queryset = Column.objects.filter(
            board_id=card_board)
        # attachemnts
        attachment_form = AttachmentForm()
        # tracker stuff
        tracker = Tracker.objects.all().filter(object_id=card.id)

        boards = Board.objects.all().filter(archived=False)
        context_dict = {
            'site_title': "Cards | Spearhead Systems",
            'page_name': "Edit Card",
            'card': card,
            'editcard_form': editcard_form,
            'attachments': attachments,
            'attachment_form': attachment_form,
            'comment_form': comment_form,
            'watchers': card_watchers,
            'tracker': tracker,
            'comments': comments,
            'boards': boards,
            'SITE_URL': SITE_URL,

        }
        return render(request, 'cards/editcard.html', context_dict)
    # if user is customer and user is in watchers allow
    # if user is org_admin and user.org is card.org allow
    elif request.user.profile_user.is_customer and request.user in instance.watchers.all() or \
            request.user.profile_user.is_org_admin and request.user.profile_user.company == instance.company:
        # print("editcard main IF >>>> ")
        card = instance
        if card.company == request.user.profile_user.company:
            ctype = ContentType.objects.get_for_model(card)
            attachments = Attachment.objects.filter(
                card=card.id)
            comments = Comment.objects.filter(
                content_type__pk=ctype.id,
                object_id=card.id,
                public=True
            )
            editcard_form = EditCardForm(instance=instance)
            editcard_form.fields['watchers'].queryset = User.objects.filter(is_active=True)
            editcard_form.fields['owner'].queryset = User.objects.filter(is_staff=True)
            # comments
            comment_form = CommentForm()
            card_watchers = User.objects.all().filter(Watchers=card.id)
            # get board id
            card_board = card.board_id
            editcard_form.fields["column"].queryset = Column.objects.filter(
                board_id=card_board)
            # tracker stuff
            tracker = Tracker.objects.filter(object_id=card.id)
            # end tracker stuff
            # attachments
            attachment_form = AttachmentForm()

            context_dict = {
                'site_title': "Cards | Spearhead Systems",
                'page_name': "editcard-ext",
                'card': card,
                'editcard_form': editcard_form,
                'boards': boards,
                'attachments': attachments,
                'comment_form': comment_form,
                'watchers': card_watchers,
                'tracker': tracker,
                'comments': comments,
                'attachment_form': attachment_form,
                'SITE_URL': SITE_URL,
            }
            return render(request, 'cards/editcard-ext.html', context_dict)
            # if superuser or operator
        elif request.user in instance.watchers.all():
            card = instance
            ctype = ContentType.objects.get_for_model(card)
            attachments = Attachment.objects.filter(
                card=card.id)
            comments = Comment.objects.filter(
                content_type__pk=ctype.id,
                object_id=card.id,
                public=True
            )
            editcard_form = EditCardForm(instance=instance)
            editcard_form.fields['watchers'].queryset = User.objects.filter(is_active=True)
            editcard_form.fields['owner'].queryset = User.objects.filter(is_staff=True)
            # comments
            comment_form = CommentForm()
            card_watchers = User.objects.all().filter(Watchers=card.id)
            # get board id
            card_board = card.board_id
            editcard_form.fields["column"].queryset = Column.objects.filter(
                board_id=card_board)
            # tracker stuff
            tracker = Tracker.objects.filter(object_id=card.id)
            # end tracker stuff
            # attachments
            attachment_form = AttachmentForm()
            context_dict = {
                'site_title': "Cards | Spearhead Systems",
                'page_name': "editcard-ext",
                'card': card,
                'editcard_form': editcard_form,
                'attachments': attachments,
                'comment_form': comment_form,
                'watchers': card_watchers,
                'tracker': tracker,
                'comments': comments,
                'attachment_form': attachment_form,
                'boards': boards,
                'SITE_URL': SITE_URL,
            }
            return render(request, 'cards/editcard-ext.html', context_dict)
    elif request.user.profile_user.company == instance.company:
        card = instance
        ctype = ContentType.objects.get_for_model(card)
        attachments = Attachment.objects.filter(
            card=card.id)
        comments = Comment.objects.filter(
            content_type__pk=ctype.id,
            object_id=card.id,
            public=True
        )
        editcard_form = EditCardForm(instance=instance)
        editcard_form.fields['watchers'].queryset = User.objects.filter(is_active=True)
        editcard_form.fields['owner'].queryset = User.objects.filter(is_staff=True)
        # comments
        comment_form = CommentForm()
        card_watchers = User.objects.all().filter(Watchers=card.id)
        # get board id
        card_board = card.board_id
        editcard_form.fields["column"].queryset = Column.objects.filter(
            board_id=card_board)
        # tracker stuff
        tracker = Tracker.objects.filter(object_id=card.id)
        # end tracker stuff
        # attachments
        attachment_form = AttachmentForm()
        context_dict = {
            'site_title': "Cards | Spearhead Systems",
            'page_name': "editcard-ext",
            'card': card,
            'editcard_form': editcard_form,
            'attachments': attachments,
            'comment_form': comment_form,
            'watchers': card_watchers,
            'tracker': tracker,
            'comments': comments,
            'attachment_form': attachment_form,
            'SITE_URL': SITE_URL,
        }
        return render(request, 'cards/editcard-ext.html', context_dict)
    else:
        return HttpResponse("You do not have permissions to view this page.")


@login_required
def getCardSlaStatus(request, card=None):
    if request.user.profile_user.is_operator:
        if card:
            try:
                card = Card.objects.get(id=card).sla_breached()
                results = card
            except ObjectDoesNotExist:
                results = 0
            data = json.dumps(results)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponse("You do not have permissions to view this page.")


@login_required
@staff_member_required
def editColumn(request, column=None):
    """
    Edit a column. Edit the properties of a column.
    """
    current_url = resolve(request.path_info).url_name
    instance = Column.objects.get(id=column)
    # request.is_ajax() or
    if request.method == 'POST':
        editColumnForm = EditColumnForm(request.POST, instance=instance)
        if editColumnForm.is_valid():
            editColumnForm.save(commit=True)
            return HttpResponseRedirect("/cards/")
        # else:
            # TODO: something meaningful perhaps
            # print(editColumnForm.errors)
        # this should never hit
        return HttpResponseRedirect("/home/")
    else:
        # print instance
        # if we are here it means nothing was posted
        # and we need to present the editcardform
        context = RequestContext(request)
        col = Column.objects.get(id=column)
        editColumnForm = EditColumnForm(instance=instance)
        context_dict = {
            'site_title': "Column | Spearhead Systems",
            'page_name': "Edit column",
            'active_url': current_url,
            'editColumnForm': editColumnForm,
            'col': col, }
        return render(request, 'cards/editcolumn.html',context_dict)

@login_required
@staff_member_required
# get attachments view
def get_attachments(request):
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('term', '')
        attachments = Attachment.objects.all().select_related().filter(
            card__id=q)
        data = serializers.serialize("json", attachments)
        # card = Card.objects.get(id=61)
        # print attachments
        data = json.dumps(data)
    else:
        data = 'fail'
    # mimetype = 'application/json'
    return HttpResponse(data, content_type='application/json')


@login_required
@staff_member_required
# get users view
# TODO: move to contacts view
def get_users(request):
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('q', '')
        user = User.objects.filter(
            Q(is_staff=True),
            first_name__icontains=q)
        results = []
        for us in user:
            co_json = {}
            co_json['id'] = us.id
            co_json['name'] = us.first_name + ' ' + us.last_name
            # co_json['value'] = us.id
            results.append(co_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    # mimetype = 'application/json'
    return HttpResponse(data, content_type='application/json')

# todo this can be removed
@login_required
@staff_member_required
def get_watchers(request):
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('card', '')
        card = Card.objects.get(id=q)
        watchers = User.objects.all().filter(Watchers=card.id)
        results = []
        for watcher in watchers:
            co_json = {}
            co_json['id'] = watcher.id
            co_json['name'] = watcher.first_name + ' ' + watcher.last_name
            # co_json['value'] = us.id
            results.append(co_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    # mimetype = 'application/json'
    return HttpResponse(data, content_type='application/json')

# mailgun
# Handler for HTTP POST to http://myhost.com/messages for the
# route defined above

@csrf_exempt # TODO: add csrf token
def mailpost(request):
    """
    Handles incoming email from Mailgun: create a new card, add
    and/or create watchers based on organization settings.
    """
    # TODO: this is pretty unmanageable long-term/ break it down to functions
    # TODO: search for open cards and ALSO 3 days back!
    if request.method == 'POST':
        sender = request.POST.get('sender')
        sender_from = request.POST.get('from')
        # recipient = request.POST.get('recipient')
        cc = request.POST.getlist('Cc')
        subject = request.POST.get('subject', '')
        body_plain = request.POST.get('body-plain', '')
        body_html = request.POST.get('body-html', '')
        body_plain_stripped = request.POST.get('stripped-text', '')
        # we use stripped html in replies
        body_html_stripped = request.POST.get('stripped-html', '')

        # TODO: maybe strip signatures on replies?
        # sender_signature = request.POST.get('stripped-html   ', '')
        # note: other MIME headers are also posted here...
        # is there an html part? if this is a reply to an existing conversation
        # we only want the reply .. etc

        # TODO: for our MVP plain is just fine
        body_html = body_plain
        # if not body_html:
        #     body_html = body_plain
        # if not body_html_stripped:
        #     body_html_stripped = body_plain_stripped
        # body_html_stripped = body_plain_stripped

        parsed_sender = parseaddr(sender_from)
        parsed_sender_email = parsed_sender[1]
        domain = parsed_sender[1].split('@')[1]
        watchers = []
        card = re.findall(doit_email_subject_keyword + '(\\d+)', subject)

        if card:
            existing_card = Card.objects.get(id=card[0])
            # if card.is_closed reopen, put on column.board/?
        else:
            existing_card = None
        try:
            user = User.objects.get(email=str(parsed_sender_email.lower()))
        except ObjectDoesNotExist:
            user = None
        if user:
            try:
                company = user.profile_user.company
            except ObjectDoesNotExist:
                company = None
        whatami = ContentType.objects.get(model="Card")

        if existing_card is not None:
            if user and user.is_active is not False:
                comment_object = Comment.objects.create(
                    owner=user,
                    comment=body_html_stripped,
                    public=True,
                    minutes=0,
                    overtime=False,
                    billable=False,
                    content_type=whatami,
                    object_id=int(existing_card.id)
                )
                comment_object.save()
                # TODO: check watchers (external contacts) - turn this into a function maybe
                randpass = User.objects.make_random_password()
                for i in getaddresses(cc):
                    try:
                        watcher = User.objects.get(email=str(i[1]).lower())
                        watchers.append(watcher)
                    except ObjectDoesNotExist:
                        randpass = User.objects.make_random_password()
                        # create the contact here
                        user = User.objects.create_user(
                            str(i[1]).lower(),
                            str(i[1]).lower(),
                            randpass
                        )
                        user.save()
                        profile = UserProfile.objects.create(
                            user=user,
                            is_customer=True
                        )
                        profile.save()
                        watcher = User.objects.get(email=str(i[1]).lower())
                        watchers.append(watcher)
                        message = """
                                    ## Please do not reply to this email ##

                                    Below are your account details for your Spearhead DoIT account.

                                    Username: %s
                                    Password: %s
                                    URL: %s

                                    # This is a message from Spearhead DoIT.

                                                    """
                        formatted_message = message % (
                            user.email,
                            randpass,
                            SITE_URL)
                        send_mail(
                            'Your new DoIT account is ready',
                            formatted_message,
                            "no-reply@spearhead.systems",
                            [user.email],
                            fail_silently=False)
                if watchers:
                    for w in watchers:
                        w.Watchers.add(existing_card)
                        w.save()
                # attachments
                for key in request.FILES:
                    # file = u' '.join(request.FILES[key]).encode('utf-8').strip()
                    file = request.FILES[key]
                    mime = file.content_type
                    Attachment.objects.create(
                        name=file.name,
                        content=file,
                        uploaded_by=user,
                        card=existing_card,
                        mimetype=mime,
                    )

                lib.sendmail_card_updated(existing_card.id, comment_object)
            else:
                # this means that the card exists but our user is not.active
                message = """
                           ## Please do not reply to this email ##
                           
                           Dear Sender,

                           A valid account was not found for your email address in our systems.
                        
                           If you believe this message is in error please reach out to our support staff at
                           help@spearhead.systems.
                           """
                send_mail(
                    'Failed to deliver your message',
                    message,
                    "no-reply@spearhead.systems",
                    [parsed_sender_email],
                    fail_silently=False)
        else:
            # the card does not exist , check if the user exists
            if user and user.is_active is not False:
                # if we have default_board use it otherwise use global)
                try:
                    board_columns = Column.objects.filter(board=user.profile_user.company.default_board)
                except AttributeError:
                    board_columns = Column.objects.filter(board=doit_default_board)

                # if board_columns.get(id) == doit_default_board:
                #     print("board_columns == doit_default_board")

                try:
                    column_type_queue = Columntype.objects.get(name="Queue")
                    # board_columns = Column.objects.filter(board=user.profile_user.company.default_board)
                    board = user.profile_user.company.default_board
                    queue_column = board_columns.get(usage=column_type_queue)
                except (AttributeError, ObjectDoesNotExist) as e:
                    column_type_queue = Columntype.objects.get(name="Queue")
                    board_columns = Column.objects.filter(board=doit_default_board)
                    queue_column = board_columns.get(usage=column_type_queue)
                    board = Board.objects.get(id=doit_default_board)

                # new card
                card = Card.objects.create(
                    created_by_id=user.id,
                    board_id=board.id,
                    column_id=str(queue_column.id),
                    title=subject,
                    description=body_html,
                    estimate="240",
                    csat='0'
                )
                card.save()

                # add sender as watcher
                watcher = User.objects.get(email=str(parsed_sender_email).lower())
                watchers.append(watcher)
                # TODO: check watchers (external contacts) - turn this into a function maybe
                randpass = User.objects.make_random_password()
                for i in getaddresses(cc):
                    try:
                        watcher = User.objects.get(email=str(i[1]).lower())
                        watchers.append(watcher)
                    except ObjectDoesNotExist:
                        randpass = User.objects.make_random_password()
                        # create the contact here
                        user = User.objects.create_user(
                            str(i[1]).lower(),
                            str(i[1]).lower(),
                            randpass
                        )
                        user.save()
                        profile = UserProfile.objects.create(
                            user=user,
                            is_customer=True
                        )
                        profile.save()
                        watcher = User.objects.get(email=str(i[1]).lower())
                        watchers.append(watcher)
                        message = """
                                       ## Please do not reply to this email ##

                                       Below are your account details for your Spearhead DoIT account.

                                       Username: %s
                                       Password: %s
                                       URL: %s

                                       # This is a message from Spearhead DoIT.

                                       """
                        formatted_message = message % (
                            user.email,
                            randpass,
                            SITE_URL)
                        send_mail(
                            'Your new DoIT account is ready',
                            formatted_message,
                            "no-reply@spearhead.systems",
                            [user.email],
                            fail_silently=False)
                if watchers:
                    for w in watchers:
                        w.Watchers.add(card)
                        w.save()

                # attachments
                for key in request.FILES:
                    Attachment.objects.create(
                        name=request.FILES[key],
                        content=request.FILES[key],
                        uploaded_by=user,
                        card=card,
                        mimetype=request.FILES[key].content_type
                    )
                lib.sendmail_card_created(card.id, user)
            else:
                # this means user does not exist we should create him
                # we should create watchers
                randpass = User.objects.make_random_password()
                # create the contact here
                user = User.objects.create_user(
                    str(parsed_sender_email).lower(),
                    str(parsed_sender_email).lower(),
                    randpass
                )
                user.save()
                profile = UserProfile.objects.create(
                    user=user,
                    is_customer=True
                )
                profile.save()


                column_type_queue = Columntype.objects.get(name="Queue")
                board_columns = Column.objects.filter(board=doit_default_board)
                queue_column = board_columns.get(usage=column_type_queue)
                board = Board.objects.get(id=doit_default_board)


                # new card
                card = Card.objects.create(
                    created_by_id=user.id,
                    board_id=board.id,
                    column_id=str(queue_column.id),
                    title=subject,
                    description=body_html,
                    estimate="240",
                    csat='0'
                )

                card.save()
                watcher = User.objects.get(email=parsed_sender_email.lower())
                watchers.append(watcher)

                message = """
                           ## Please do not reply to this email ##

                           Below are your account details for your Spearhead DoIT account.

                           Username: %s
                           Password: %s
                           URL: %s

                           # This is a message from Spearhead DoIT.

                           """
                formatted_message = message % (
                    user.email,
                    randpass,
                    "https://doit.spearhead.systems/")
                send_mail(
                    'Your new DoIT account is ready',
                    formatted_message,
                    "no-reply@spearhead.systems",
                    [user.email],
                    fail_silently=False)

                # card doesnt exist:
                column_type_queue = Columntype.objects.all().filter(name="Queue")
                board_columns = Column.objects.filter(board=doit_default_board)
                queue_column = board_columns.get(usage=column_type_queue)
                board = Board.objects.get(id=doit_default_board)

                # new card
                card = Card.objects.create(
                    created_by_id=1,
                    board_id=board.id,
                    column_id=str(queue_column.id),
                    title=subject,
                    description=body_html,
                    estimate="240",
                    csat='0'
                )
                card.save()
                # add sender as watcher
                watcher = User.objects.get(email=str(parsed_sender_email).lower())
                watchers.append(watcher)

                for i in getaddresses(cc):
                    try:
                        watcher = User.objects.get(email=str(i[1]).lower())
                        watchers.append(watcher)
                    except ObjectDoesNotExist:
                        randpass = User.objects.make_random_password()
                        # create the contact here
                        user = User.objects.create_user(
                            str(i[1]).lower(),
                            str(i[1]).lower(),
                            randpass
                        )
                        user.save()
                        profile = UserProfile.objects.create(
                            user=user,
                            is_customer=True
                        )
                        profile.save()
                        watcher = User.objects.get(email=str(i[1]).lower())
                        watchers.append(watcher)
                        message = """
                                       ## Please do not reply to this email ##

                                       Below are your account details for your Spearhead DoIT account.

                                       Username: %s
                                       Password: %s
                                       URL: %s

                                       # This is a message from Spearhead DoIT.

                                       """
                        formatted_message = message % (
                            user.email,
                            randpass,
                            "https://doit.spearhead.systems/")
                        send_mail(
                            'Your new DoIT account is ready',
                            formatted_message,
                            "no-reply@spearhead.systems",
                            [user.email],
                            fail_silently=False)
                if watchers:
                    for w in watchers:
                        w.Watchers.add(card)
                        w.save()

                # attachments
                for key in request.FILES:
                    file = request.FILES[key]
                    mime = file.content_type
                    Attachment.objects.create(
                        name=file.name,
                        content=file,
                        uploaded_by=user,
                        card=card,
                        mimetype=mime,
                    )
                lib.sendmail_card_created(card.id, user)

    return HttpResponse('OK')
