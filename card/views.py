from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import resolve
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, render
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
from card.models import Card, Column, Organization, Board, Task, \
    Columntype, Reminder
# from card.forms import CardsForm
from comment.models import Comment
from contact.models import UserProfile
from attachment.models import Attachment
from attachment.forms import AttachmentForm
from comment.forms import CommentForm
# forms
from forms import CardsForm, ColumnForm, EditCardForm, \
    EditColumnForm, BoardFormSet, ReminderForm
# date stuff
from datetime import date, datetime, timedelta
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

# GLOBALS
doitVersion = settings.DOIT_VERSION
doit_myemail = settings.DOIT_MYEMAIL


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
        cards = Card.objects.all().prefetch_related().filter(
            ~Q(column__usage=columnDone),
        )

        context = RequestContext(request)
        context_dict = {
            'site_title': "Cards | Spearhead Systems",
            'page_name': "BoB",
            'cards': cards,
            'doitVersion': doitVersion,
        }
        return render(request, 'boards/bob.html', context_dict, context)

    boards = Board.objects.filter(archived=False)

    if request.user.profile_user.is_operator:
        numbers_list = Card.objects.all().filter(board=board_id).filter(closed=True)[:10]
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
        all_cards_but_deleted = Card.objects.select_related().filter(
            ~Q(column_id=done_column), Q(board=board_id)
        )
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
        cards = sorted(cardslist, key=lambda x: x.order, reverse=False)
    else:
        u = User.objects.get(username=request.user)
        up = UserProfile.objects.get(user=u)
        # check for user as owner or watcher/contact on board
        board = Board.objects.get(id=board_id)
        if u.id != board.owner.id:
            return HttpResponse("You do not have permissions to view this page.")

        # end check user perms

        numbers_list = Card.objects.filter(board=board_id).filter(closed=True).filter(owner=request.user)[:10]
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
        all_cards_but_deleted = Card.objects.select_related().filter(
            ~Q(column_id=done_column),
            Q(board=board_id),
        ).filter(owner=u)
        gg = Card.objects.filter(closed=False).filter(watchers__id__exact=request.user.id)
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
        cards = sorted(cardslist, key=lambda x: x.order, reverse=False)

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
    return render(request, 'cards/cards.html', context_dict, context)


@login_required
@staff_member_required
def calendar(request, year=2017, month=1):
    my_cards = Card.objects.order_by('due_date').filter(
        due_date__year=year, due_date__month=month
    )
    cal = CardCalendar(my_cards).formatmonth(year, month)
    return render_to_response(
        'cards/calendar.html',
        {'calendar': mark_safe(cal), }
    )


# tags for autocomplete
class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

# watchers for autocomplete
class WatcherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        qs = User.objects.all().filter(is_active=True)

        if self.q:
             qs = qs.filter(username__icontains=self.q)

        return qs

# company for autocomplete
class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        qs = Organization.objects.all().filter(active=True)

        if self.q:
             qs = qs.filter(name__icontains=self.q)

        return qs

# owner for autocomplete
class OwnerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Tag.objects.none()

        qs = User.objects.all().filter(is_active=True).filter(profile_user__is_operator=True)

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
        card_due_date = (request.POST['due_date'])
        card_start_time = (request.POST['start_time'])
        card_tags = (request.POST.getlist('tags'))

        try:
            card_company = request.POST['company']
        except KeyError:
            card_company = None
        card_board = request.POST['board']
        try:
            card_owner = request.POST['owner']
            # print card_owner
        except:
            card_owner = None

        card_watchers = request.POST.getlist('watchers')
        if not card_watchers:
            # are we a customer?
            if u.profile_user.is_customer:
                card_watchers.append(u.id)
        card_type = request.POST['type']
        card_estimate = request.POST['estimate']
        # TODO:  confirm this is ok as is

        if card_due_date == '':
            card_due_date = None

        if card_start_time == '':
            card_start_time = None

        # # if card_company is not set, we're ok with this
        if not card_company:
            card_company = None

        if not card_owner:
            card_owner = u.id

        card_created = Card.objects.create(
            owner_id=card_owner, created_by_id=u.id,
            board_id=card_board, priority_id=card_priority,
            company_id=card_company, column_id=card_column,
            title=card_title, description=card_description,
            due_date=card_due_date, start_time=card_start_time,
            type=card_type, csat='0',
            estimate=card_estimate)

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
            action=" created the card ",
            updated_fields=(' on board ') + str(
                card_created.board.name) + str(' and column ') + str(
                card_created.column.title),
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
            column_type_usage = Columntype.objects.all().filter(name="Queue")
            board_columns = Column.objects.filter(board=default_org_board.id)
            column = board_columns.get(usage=column_type_usage)
            g = Board.objects.get(id=board.id)
            org_owner = g.owner


            # we send to customer addcard form
            # addcardform = CardsForm(board_id=board, initial={'id_company:', company})
            addcardform = CardsForm(
                initial={
                    # 'owner': u.id,
                    'board': board.id,
                    'owner': org_owner,
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
                'owner': org_owner.id,
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
                'site_description': "",
                'addcardform': addcardform,
                'boards': Board.objects.filter(archived=False)
                # 'board': Board.objects.get(id=board)
            }
            return render(request, 'cards/addcard.html', context_dict)
        # not very helpful TODO something
        # return render(request, 'cards/addcard.html', context_dict)


@login_required
@staff_member_required
def add_reminder(request, card=None, **kwargs):
    """
    Add a reminder to a card.
    """
    context = RequestContext(request)
    if request.is_ajax() or request.method == 'POST':
        reminderform = ReminderForm(request.POST)
        if reminderform.is_valid():
            new_reminder = reminderform.save()

            tidy_up =  Reminder.objects.get(id=new_reminder.id)
            if not tidy_up.owner:
                tidy_up.owner = request.user
                tidy_up.save()

        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'NOK'}, status=500)


@login_required
@staff_member_required
def get_reminders(request):
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('card', '')
        card = Card.objects.get(id=q)
        u = User.objects.get(username=request.user)
        reminders = Reminder.objects.filter(
            card=card.id)
        results = []
        # TODO: if noprofile picture all goes to hell and reminders will not load
        for co in reminders:
            co_json = {}
            co_json['id'] = co.id
            # NOTE: we "force" return a localtime object since we do not go through the django template
            # therefore our datetime object here displays UTC. We use this everywhere we bypass (json/ajax)
            # a a django template
            # co_json['reminder_time'] = co.reminder_time
            co_json['reminder_time'] = str(timezone.localtime(co.reminder_time))
            co_json['owner'] = str(
                UserProfile.objects.get(user_id=co.owner_id).picture)
            results.append(co_json)
    return HttpResponse(json.dumps(results, indent=4, sort_keys=True, default=str), content_type='application/json')


@login_required
@staff_member_required
def delete_reminder(request):
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('reminder', '')
        # print("reminder is >>>> ", q)
        reminder = Reminder.objects.get(id=q)
        if reminder.delete():
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return JsonResponse({'status': 'NOK'}, status=500)
    else:
        return JsonResponse({'status': 'NOK'}, status=500)


@login_required
@staff_member_required
def addColumn(request):
    current_url = resolve(request.path_info).url_name

    if request.method == 'POST':  # If the form has been submitted...
        form = ColumnForm(request.POST)
        if form.is_valid():
            # add card to database
            # obj = model(**form.cleaned_data)
            # model_instance = form.save(commit=False)
            # model_instance =
            form.save()

            return HttpResponseRedirect('/cards/')

    context = RequestContext(request)
    formSet = BoardFormSet()
    form = ColumnForm()
    context_dict = {
        'site_title': "Cards | Spearhead Systems",
        'page_name': "Add a Column",
        'active_url': current_url,
        'site_description': "",
        'form': form,
        'formSet': formSet, }
    # return render_to_response('cards/addcolumn.html', context_dict, context)
    return render(request, 'cards/addcolumn.html', context_dict, context)


@login_required
@staff_member_required
def deleteCard(request):
    """
    Delete a card.

    """

    current_url = resolve(request.path_info).url_name

    if request.is_ajax() or request.method == 'POST':
        card = request.POST['card']

        # TODO: make sure user has permission to add this comment
        # by looking at watchers, company with is_org_admin

        # ajaxifying shit up
        xhr = request.GET.has_key('xhr')

        # select card
        workon_card = Card.objects.get(id=card)
        workon_card.delete()
        # save our work
        # workon_card.save()

        # if we were called via ajax
        # then pop up a little OK or something
        if xhr:
            return HttpResponse(
                simplejson.dumps(response_dict),
                mimetype='application/javascript')

        return HttpResponseRedirect("/cards/deletecard/")
    # print the form - nothing was submitted to POST
    else:
        context = RequestContext(request)
        cards = Card.objects.all()
        columns = Column.objects.all()
        context_dict = {
            'site_title': "Cards | Spearhead Systems",
            'page_name': "Add Card",
            'active_url': current_url,
            'site_description': "",
            'columns': columns,
            'cards': cards, }
        return render_to_response(
            'cards/deletecard.html', context_dict, context)


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
            'site_description': "",
            'columns': columns,
            'cards': cards, }
        # return render_to_response(
        #     'cards/movecard.html', context_dict, context)
        return render(request, 'cards/movecard.html', context_dict)


@login_required
def movecardtoboard(request):
    print("in the movecardtoboard view >>>> ")
    if request.is_ajax() or request.method == 'POST':
        card = request.POST['card']
        board = request.POST['board']
        column = request.POST['column']
        workon_card = Card.objects.get(id=card)
        workon_column = Column.objects.get(id=column)
        workon_board = Board.objects.get(id=board)
        new_column = Column.objects.get(id=column)
        previous_column = workon_card.column
        # print("moving card %s from board %s to board %s and column %s") % (workon_card, workon_card.board, workon_board, workon_column)
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
            action_text=' from ' + str(previous_column) + ' to ' + str(workon_column)
            workon_card.column = workon_column
            workon_card.board = workon_board
            workon_card.save()

        # MOVE CREATED TRACKER
        ctype = ContentType.objects.get_for_model(workon_card)
        tracker = Tracker.objects.create(
            created_time=datetime.now(),
            content_type=ctype,
            object_id=workon_card.id,
            updated_fields=str(action_text),
            owner=request.user,
            action=str(" moved card from board %s " % workon_board),
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
        return render_to_response('cards/order.html')


@login_required
def closecard(request, card=None):
    card = Card.objects.get(id=card)
    done_column = Column.objects.all().filter(
        board=card.board.id).filter(usage__name="Done")
    # TODO: wtf, this needs cleaning
    # by looking at watchers, company with is_org_admin
    if request.user.profile_user.is_customer and \
        request.user.profile_user.is_org_admin:
        # check card company and watcher

        if card in request.user.Watchers.all():
            print "we're in"

    card.column = done_column[0]
    card.closed = True
    card.save()

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
        'page_name': "Edit Card",
        'site_description': "",
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
    # TODO: wtf, this needs cleaning
    # by looking at watchers, company with is_org_admin
    if request.user.profile_user.is_customer and \
        request.user.profile_user.is_org_admin:

        if card in request.user.Watchers.all():
            card.column = queue_column[0]
            card.closed = False
            card.save()
        else:
            return HttpResponse("Well now this is embarrassing :-/ ." \
                                "Please let help@spearhead.systems know about this issue. " \
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
    previous_column = Card.objects.get(id=card).column.usage
    boards = Board.objects.filter(archived=False)

    # if request.method == 'POST':
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
            elif str(previous_column) != "Done" and str(instance.column) == "Done":
                action_text = str(" closed the card ")
                instance.closed = True
                instance.save()
            elif str(previous_column) == "Done" and str(instance.column) == "Done":
                action_text = str(" updated already closed card ")
                instance.closed = True
                instance.save()
            elif str(previous_column) == "Done" and str(instance.column) != "Done":
                action_text = str(" reopened closed card and placed it in the ") + str(instance.column) + str(" column ")
                instance.closed = False
                instance.save()
            else:
                action_text=str(" edited the card ")
            ctype = ContentType.objects.get_for_model(instance)
            tracker = Tracker.objects.create(
                created_time=datetime.now(),
                content_type=ctype,
                object_id=instance.id,
                updated_fields=str(" updated ") + str(form.changed_data),
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
            }
            return HttpResponse(render_to_string(form.errors, context_dict, RequestContext(request)))

        if request.is_ajax():
            return JsonResponse({'status': 'ok'})
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.user.profile_user.is_operator:
        card = Card.objects.select_related().get(id=card)
        ctype = ContentType.objects.get_for_model(card)
        addreminder_form = ReminderForm()
        attachments = Attachment.objects.filter(
            card=card.id)
        # print("attachments >>>> ", attachments)
        comments = Comment.objects.filter(content_type__pk=ctype.id, object_id=card.id)
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
        tracker = Tracker.objects.prefetch_related().filter(object_id=card.id)
        boards = Board.objects.all().filter(archived=False)
        context_dict = {
            'site_title': "Cards | Spearhead Systems",
            'page_name': "Edit Card",
            'site_description': "",
            'card': card,
            'editcard_form': editcard_form,
            'attachments': attachments,
            'attachment_form': attachment_form,
            'comment_form': comment_form,
            'watchers': card_watchers,
            'tracker': tracker,
            'comments': comments,
            'addreminder_form': addreminder_form,
            'boards': boards,

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
            addreminder_form = ReminderForm()
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
                'site_description': "",
                'card': card,
                'editcard_form': editcard_form,
                'boards': boards,
                'attachments': attachments,
                'comment_form': comment_form,
                'watchers': card_watchers,
                'tracker': tracker,
                'comments': comments,
                'addreminder_form': addreminder_form,
                'attachment_form': attachment_form,
            }
            return render(request, 'cards/editcard-ext.html', context_dict)
            # if superuser or operator
        elif request.user in instance.watchers.all():
            print("as  a card contact only I am in!!!! >>>>>")
            card = instance

            ctype = ContentType.objects.get_for_model(card)
            addreminder_form = ReminderForm()
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
                'site_description': "",
                'card': card,
                'editcard_form': editcard_form,
                'attachments': attachments,
                'comment_form': comment_form,
                'watchers': card_watchers,
                'tracker': tracker,
                'comments': comments,
                'addreminder_form': addreminder_form,
                'attachment_form': attachment_form,
                'boards': boards,
            }
            return render(request, 'cards/editcard-ext.html', context_dict)
    elif request.user.profile_user.company == instance.company:
        print("as  a company contanct I am in!!!! >>>>>")
        card = instance

        ctype = ContentType.objects.get_for_model(card)
        addreminder_form = ReminderForm()
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
            'site_description': "",
            'card': card,
            'editcard_form': editcard_form,
            'attachments': attachments,
            'comment_form': comment_form,
            'watchers': card_watchers,
            'tracker': tracker,
            'comments': comments,
            'addreminder_form': addreminder_form,
            'attachment_form': attachment_form,
        }
        return render(request, 'cards/editcard-ext.html', context_dict)
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
        else:
            # TODO: something meaningful perhaps
            print editColumnForm.errors
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
            'site_description': "",
            'editColumnForm': editColumnForm,
            'col': col, }
        return render_to_response(
            'cards/editcolumn.html', context_dict, context)


# # not currently used - but maybe could be tied into a
# # self-service portal -- approval sent to company admin?
# def register(request):
#     # Like before, get the request's context.
#     context = RequestContext(request)
#
#     # A boolean value for telling the template whether the registration
#     #  was successful. Set to False initially. Code changes value to
#     # True when registration succeeds.
#     registered = False
#
#     # If it's a HTTP POST, we're interested in processing form data.
#     if request.method == 'POST':
#         # Attempt to grab information from the raw form information.
#         # Note that we make use of both UserForm and UserProfileForm.
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         # If the two forms are valid...
#         if user_form.is_valid() and profile_form.is_valid():
#             # Save the user's form data to the database.
#             user = user_form.save()
#
#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()
#
#             # Now sort out the UserProfile instance.
#             # Since we need to set the user attribute ourselves, we set
#             #  commit=False.
#             # This delays saving the model until we're ready to avoid
#             #  integrity problems.
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             # Did the user provide a profile picture?
#             # If so, we need to get it from the input form and put it
#             # in the UserProfile model.
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             # Now we save the UserProfile model instance.
#             profile.save()
#
#             # Update our variable to tell the template registration
#             # was successful.
#             registered = True
#
#         # Invalid form or forms - mistakes or something else?
#         # Print problems to the terminal.
#         # They'll also be shown to the user.
#         else:
#             print user_form.errors  # , #profile_form.errors
#
#     # Not a HTTP POST, so we render our form using two ModelForm
#     # instances. These forms will be blank, ready for user input.
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     # Render the template depending on the context.
#     return render_to_response('cards/register.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'registered': registered
#     },
#           # {'user_form': user_form, 'registered': registered},
#                               context)

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


@login_required
@staff_member_required
# @csrf_exempt
def addtask(request, card=None, **kwargs):
    """
    Add a task
    :param request:
    :param card:
    :param kwargs:
    :return:
    """
    # current_url = resolve(request.path_info).url_name
    if request.is_ajax() or request.method == 'POST':
        # get the user if not then use request.user
        userid = request.user
        card = request.POST['card']
        print("this is the card >>>>> ", card)
        card_object = Card.objects.get(id=card)
        task = request.POST['task']
        ctype = ContentType.objects.get_for_model(card_object)
        taskg_obj = Task.objects.create(
            task=task,
            content_type=ctype,
            object_id=card_object.id,
            owner=userid
        )
        # ADD TASK TRACKER
        ctype = ContentType.objects.get_for_model(taskg_obj)
        # updates = {
        #   'task': taskg_obj.task,
        #   'done': taskg_obj.done,
        #   'owner': int(taskg_obj.owner.id),
        # }

        tracker = Tracker.objects.create(
            created_time=datetime.now(),
            content_type=ctype,
            object_id=card_object.id,
            action=str(" created a task "),
            updated_fields=str(taskg_obj),
            owner=userid,
        )
        tracker.save()
        # END ADD TASK TRACKER

        # TODO: return something meaningul
        # return render_to_response('cards/task.html')
        return JsonResponse({'status': 'OK'})
    else:
        return JsonResponse({'status': 'NOK'}, status=500)


@login_required
@staff_member_required
# @csrf_exempt
def update_task(request):
    """
    Update a task
    """
    # current_url = resolve(request.path_info).url_name
    if request.is_ajax() or request.method == 'POST':
        # xhr = request.POST.has_key('xhr')
        # userid = request.user
        task = request.POST['task']
        status = request.POST['status']
        task_obj = Task.objects.get(id=task)

        if status == "True":
            task_obj.done = bool(1)
            tracker_text = str(" finished task ") + str(task_obj)
            task_obj.save()
        else:
            task_obj.done = bool(0)
            tracker_text = str(" reopened task ") + str(task_obj)
            task_obj.save()

        # UPDATE TASK TRACKER
        # TODO: how do i get card id/name?
        ctype = ContentType.objects.get_for_model(task_obj)
        tracker = Tracker.objects.create(
            created_time=datetime.now(),
            content_type=ctype,
            object_id=task_obj.object_id,
            action=tracker_text,
            updated_fields=str(''),
            owner=request.user,
        )
        tracker.save()
        # END UPDATE TASK TRACKER

        # TODO: return something meaningul
        # return render_to_response('cards/task.html')
        return JsonResponse({'status': 'OK'})


@login_required
def get_tasks(request):
    # context = RequestContext(request)
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('card', '')
        card = Card.objects.get(id=q)
        # what is this?
        ctype = ContentType.objects.get_for_model(card)
        tasks = Task.objects.filter(
            content_type__pk=ctype.id,
            object_id=card.id)
        results = []
        for co in tasks:
            co_json = {}
            co_json['id'] = co.id
            co_json['task'] = co.task
            co_json['done'] = co.done
            co_json['created_time'] = str(co.created_time)
            picture = UserProfile.objects.get(user_id=co.owner.id)
            co_json['owner'] = str(picture.picture)
            results.append(co_json)
        data = json.dumps(results)
    return HttpResponse(data, content_type='application/json')

@login_required
def get_task_count(request):
    context = RequestContext(request)
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('card', '')
        card = Card.objects.get(id=q)
        ctype = ContentType.objects.get_for_model(card)
        tasks = Task.objects.filter(
            content_type__pk=ctype.id,
            object_id=card.id)
        results = [tasks.count()]
        data = json.dumps(results)
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
        body_html_stripped = body_plain_stripped

        parsed_sender = parseaddr(sender_from)
        parsed_sender_email = parsed_sender[1]
        domain = parsed_sender[1].split('@')[1]
        watchers = []
        card = re.search('#doit(\\d+)', subject)

        if card:
            existing_card = Card.objects.get(id=card.group(1))
        else:
            existing_card = None
        try:
            user = User.objects.get(email=str(parsed_sender_email.lower()))
        except ObjectDoesNotExist:
            user = None
        try:
            company = Organization.objects.get(email_domains__domain__icontains=domain)
        except ObjectDoesNotExist:
            company = None

        print("#--------- emails>>>>>> ")
        print("sender_from >> ", sender_from)
        print("sender >> ", sender)
        print("cc > ", cc)
        print("parsed_sender > ", parsed_sender)
        print("parsed_sender_email > ", parsed_sender_email)
        print("domain > ", domain)
        print("user > ", user)

        whatami = ContentType.objects.get(model="Card")

        # check if a card exists and if so forgo all other checks
        # except maybe for (new) watchers
        if existing_card:
            if user and user.is_active:
                column_type_queue = Columntype.objects.all().filter(name="Queue")
                try:
                    board_columns = Column.objects.filter(board=str(user.profile_user.company.default_board.id))
                except:
                    board_columns = Column.objects.filter(board=1)
                queue_column = board_columns.get(usage=column_type_queue)
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
                            "https://doit.spearhead.systems/")
                        send_mail(
                            'Your new DoIT account is ready',
                            formatted_message,
                            doit_myemail,
                            [user.email],
                            fail_silently=False)
                if watchers:
                    for w in watchers:
                        w.Watchers.add(existing_card)
                        w.save()
        else:
            # user not found, create him, card and add as watcher
            randpass = User.objects.make_random_password()
            user = User.objects.create_user(
                str(parsed_sender_email).lower(),
                str(parsed_sender_email).lower(),
                randpass
            )
            profile = UserProfile.objects.create(
                user=user,
                is_customer=True)
            profile.save()
            message = """
                        ## Please do not reply to this email ##

                        Below are your account details for your Spearhead DoIT account.

                        Username: %s
                        Password: %s
                        URL: %s

                        # This is a message from Spearhead DoIT. Please do not reply to
                        this message, instead use the above link. 

                        """
            formatted_message = message % (
                user.email,
                randpass,
                "https://doit.spearhead.systems/")
            send_mail(
                'Your new DoIT account is ready',
                formatted_message,
                doit_myemail,
                [user.email],
                fail_silently=False)
            column_type_queue = Columntype.objects.all().filter(name="Queue")
            board_columns = Column.objects.filter(board=1)
            queue_column = board_columns.get(usage=column_type_queue)
            whatami = ContentType.objects.get(model="Card")

            # new card
            card = Card.objects.create(
                created_by_id=user.id,
                board_id=1,
                column_id=str(queue_column.id),
                title=subject,
                description=body_html,
                estimate="240",
                csat='0'
            )
            card.save()
            user.Watchers.add(card)
            # TODO: check watchers (external contacts) - turn this into a function maybe
            randpass = User.objects.make_random_password()
            for i in getaddresses(cc):
                domain = i[1].split('@')[1]
                try:
                    domain_in_company = Organization.objects.get(email_domains__domain__icontains=domain)
                except ObjectDoesNotExist:
                    domain_in_company = False

                if domain_in_company:
                    try:
                        watcher = User.objects.get(email=str(i[1]).lower())
                    except ObjectDoesNotExist:
                        randpass = User.objects.make_random_password()

                        print("watcher does not exist but allow_auto_contact_creation == true")
                        # create the contact here
                        user = User.objects.create_user(
                            str(i[1]).lower(),
                            str(i[1]).lower(),
                            randpass
                        )
                        user.save()
                        profile = UserProfile.objects.create(
                            user=user,
                            is_customer=True)
                        profile.save()
                        watcher = User.objects.get(email=str(i[1]).lower())
                        watchers.append(watcher)
                        message = """
                                    ## Please do not reply to this email ##

                                    Below are your account details for your Spearhead DoIT account.

                                    Username: %s
                                    Password: %s
                                    URL: %s

                                    # This is a message from Spearhead DoIT. Please do not reply to
                                    this message, instead use the above link. 

                                    """
                        formatted_message = message % (
                            user.email,
                            randpass,
                            "https://doit.spearhead.systems/")
                        send_mail(
                            'Your new DoIT account is ready',
                            formatted_message,
                            doit_myemail,
                            [user.email],
                            fail_silently=False)
                    if watchers:
                        for w in watchers:
                            w.Watchers.add(card)
                            w.save()
            # now we can save the m2m relations to watchers
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
            print("hitting this sendmail 002 >>>")
            lib.sendmail_card_created(card.id, user)

    return HttpResponse('OK')
