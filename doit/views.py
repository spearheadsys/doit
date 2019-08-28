from datetime import date, datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from card.models import Card, Column, Worklog, Priority, Board, Task, \
    Columntype, Comment
from contact.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import json
from django.http import JsonResponse
from doit.forms import EditUserForm, EditCustomerProfileForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count
from collections import namedtuple


# GLOBALS
doitVersion = settings.DOIT_VERSION
today_date = timezone.now()


# user login
def user_login(request):
    redirect_to = request.POST.get('next')
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your DoIT account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can
# access the view.
# @login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def settings_view(request):
    if request.user.profile_user.is_superuser:
        context_dict = {
            'site_title': "DoIT | Spearhead Systems",
            'page_name': "DoIT Settings",
            'site_description': "Spearhead DoIT",
            'doitVersion': doitVersion,
        }
        return render(request, 'settings.html', context_dict)
    elif request.user.profile_user.is_operator:
        return HttpResponse("operator")
    elif request.user.profile_user.is_customer and not request.user.profile_user.is_org_admin:
        return HttpResponse("just customer")
    elif request.user.profile_user.is_org_admin:
        return HttpResponse("orgadmin customer")
    else:
        return HttpResponse("we really should not hit here!")

@login_required
def home(request):
    # We exclude Backlog items!
    # TODO: wizard, get user/pass, create board ..
    # launch wizard here
    if request.user.is_authenticated():
        u = User.objects.get(username=request.user)
        noowner = Card.objects.all().filter(closed=False, owner=None).order_by('-due_date')
        cards = Card.objects.all().filter(closed=False, owner=u)
        boards = Board.objects.all().filter(archived=False)
        allcards = Card.objects.all().filter(closed=False)
        incidents = Card.objects.all().filter(closed=False, type="IN")
        myincidents = Card.objects.all().filter(closed=False, type="IN", owner=u)
        myboards = Board.objects.all().filter(archived=False, owner=u)
        cardswatcher = []
        for i in allcards:
            if u in i.watchers.all():
                cardswatcher.append(i)
        cardswatcher.sort(key=lambda c: c.due_date
            if (c and c.due_date)
            else timezone.now())
        mycards = []
        for i in cards:
            if str(i.column.usage) != "Backlog":
                mycards.append(i)
        mycards.sort(key=lambda c: c.due_date
            if (c and c.due_date)
            else timezone.now())
        customerowncards = []
        for i in allcards:
            if str(i.column.usage) != "Backlog" and u in i.watchers.all():
                customerowncards.append(i)
        allcustomercards = 0
        if u.profile_user.company:
            for i in allcards:
                if str(i.column.usage) != "Backlog" and i.company == u.profile_user.company:
                    allcustomercards += 1
                if str(i.column.usage) != "Backlog" and u in i.watchers.all():
                    allcustomercards += 1
        else:
            for i in allcards:
                if str(i.column.usage) != "Backlog" and u in i.watchers.all():
                    allcustomercards += 1

        myoverduecards = []
        for i in cards:
            if str(i.column.usage) != "Backlog":
                if i.is_overdue:
                    myoverduecards.append(i)
        myoverduecards.sort(key=lambda c: c.due_date
            if (c and c.due_date)
            else timezone.now())
        mycardsoverduetoday = []
        for i in cards:
            if str(i.column.usage) != "Backlog" and i.due_date:
                if i.is_overdue:
                    mycardsoverduetoday.append(i)
        alloverduecards = 0
        for i in allcards:
            if str(i.column.usage) != "Backlog" and i.due_date:
                if i.is_overdue:
                    alloverduecards +=1
        myoverdueboards = []
        for i in myboards:
            if i.is_overdue:
                myoverdueboards.append(i)
        alloverdueboards = []
        for i in boards:
            if i.is_overdue:
                alloverdueboards.append(i)
        backlogcards = []
        for i in allcards:
            if str(i.column.usage) == "Backlog":
                backlogcards.append(i)
        mybacklogcards = []
        for i in cards:
            if str(i.column.usage) == "Backlog":
                mybacklogcards.append(i)
        cardswithoutcompany = []
        for i in allcards:
            if not i.company and str(i.column.usage) != "Backlog":
                cardswithoutcompany.append(i)
        cardswithoutduedate = []
        for i in allcards:
            if not i.due_date and str(i.column.usage) != "Backlog":
                cardswithoutduedate.append(i)
        are_there_any_boards = Board.objects.all()
        if not are_there_any_boards:
            # todo: redirect to firstrun/wizard
            board_ = Board(name="Default Board")
            board_.save()

            # create default priorities
            priority_minor = Priority(title="Minor")
            priority_minor.save()
            priority_normal = Priority(title="Normal")
            priority_normal.save()
            priority_major = Priority(title="Major")
            priority_major.save()

            # create columntypes
            column_type_backlog = Columntype(name="Backlog")
            column_type_backlog.save()
            column_type_queue = Columntype(name="Queue")
            column_type_queue.save()
            column_type_working = Columntype(name="Working")
            column_type_working.save()
            column_type_waiting = Columntype(name="Waiting")
            column_type_waiting.save()
            column_type_done = Columntype(name="Done")
            column_type_done.save()

            # create default 3 columns
            column_queue = Column(title="Queue", board=board_, order="0",
                                  usage="Queue")
            # TODO: add usage!!
            column_queue.save()
            column_working = Column(title="Working", board=board_, order="1")
            column_working.save()
            column_done = Column(title="Done", board=board_, order="2")
            column_done.save()

            # we also create our groups here
            admingroup = Group()
            admingroup.name = 'Administrators'
            admingroup.save()

        startperiod = (today_date - timezone.timedelta(days=7))
        # TODO: we have users that are only looking at stuff, they appear with 0 minutes
        # we should remove them: maybe add is_working, is_active to profile?
        operators = UserProfile.objects.filter(user__is_active=True, is_operator=True)
        Operator = namedtuple("Operator", ("operator", "minutes"))
        total_minutes_per_op = []
        # TODO: this is useful as a lib somewhere
        for operator in operators:
            events = Comment.objects.filter(
                owner=operator.user,
                # created_time__range=(startperiod, today_date),
                created_time__gte=(startperiod),
                minutes__gt=0).aggregate(Sum('minutes'))
            if events['minutes__sum'] != None:
                total_minutes_per_op.append(Operator(operator, events['minutes__sum']))

        # ---
        open_card_list = Card.objects.filter(closed=False).values_list('owner', flat=True)
        group_by_owner_card_list = {}
        for value in open_card_list:
            try:
                user = User.objects.get(id=value)
                group_by_owner_card_list[str(user)] = Card.objects.filter(closed=False, owner=value).count()
            except:
                pass
                # group_by_owner_card_list[str(user)] = Card.objects.filter(closed=False, owner=value).count()
        # ---

        # ---
        top_tags = Card.tags.most_common()[:5]
        # print type(top_tags)
        # ---

        boards = Board.objects.filter(archived=False)

        context_dict = {
            'site_title': "DoIT | Spearhead Systems",
            'page_name': "DoIT",
            'site_description': "Spearhead DoIT",
            'noowner': noowner,
            'mycards': mycards,
            'customerowncards': customerowncards,
            'allcustomercards': allcustomercards,
            'myoverduecards': myoverduecards,
            'mycardsoverduetoday': mycardsoverduetoday,
            'alloverduecards': alloverduecards,
            'incidents': incidents.count(),
            'myincidents': myincidents,
            'myoverdueboards': myoverdueboards,
            'alloverdueboards': alloverdueboards,
            'cardswithoutduedate': cardswithoutduedate,
            'allcards': allcards,
            'cardswatcher': cardswatcher,
            'backlogcards': backlogcards,
            'cardswithoutcompany': cardswithoutcompany,
            'mybacklogcards': mybacklogcards,
            'total_minutes_per_op': total_minutes_per_op,
            'group_by_owner_card_list': group_by_owner_card_list,
            'top_tags': top_tags,
            'boards': boards,
            'doitVersion': doitVersion,
        }
        return render(request, 'dashboard.html', context_dict)
    else:
        return render(request, 'login.html', {})


def open_cards_ajax(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    # Note: Ordering is implicit on created_time. If we we are passed a new ordering column,
    # it is not taken into account!
    # order_column = int(request.GET['order[0][column]'])
    # TODO: not quite sure how this is supposed to works or if it works
    order_direction = '' if request.GET['order[0][dir]'] == 'desc' else '-'
    # Since these are closed cards we have unanimously voted for ordering newest closed first
    column = 'created_time'
    backlog = Columntype.objects.all().filter(name="Backlog")
    global_search = request.GET['search[value]']
    # Note: If user != superuser we limit to company or owned/watched cards only!
    if request.user.profile_user.is_operator:
        all_records = Card.objects.all().filter(closed=False).filter(
            ~Q(column__usage__exact=backlog)
        )
        records_total = all_records.count()
        if not all_records:
            all_records = 0
    # if we hit the else it means is_customer
    else:
        try:
            company = request.user.profile_user.company.id
        except:
            company = None
        if company:
            all_records = Card.objects.all().filter(
                Q(watchers__in=[request.user]) | Q(company=request.user.profile_user.company.id)
            ).filter(closed=False).exclude(column__usage__exact=backlog).distinct()
            records_total = all_records.count()
            if not all_records:
                all_records = 0
        else:
            all_records = Card.objects.all().filter(closed=False).filter(
                ~Q(column__usage__exact=backlog) &
                Q(watchers__in=[request.user.id])
            ).distinct()
            records_total = all_records.count()

    # NOTE: not sure how this is supposed to work or if it works
    # columns = [i.name for i in Card._meta.get_fields()][1:]
    # I also know this is ugly, writing/hardcoding this 3 times like this.
    columns = ['id', 'title', 'company__name', 'column__title', 'priority__title',
               'created_time', 'owner__username', 'board__name']
    objects = []
    if all_records != 0:
        if global_search:
            gret = all_records.filter(
                Q(title__icontains=global_search) |
                Q(company__name__icontains=global_search) |
                Q(column__title__icontains=global_search) |
                Q(board__name__icontains=global_search) |
                Q(owner__username__icontains=global_search) |
                Q(priority__title__icontains=global_search)
            ).order_by(order_direction + column)[start:start + length].values(
                'id',
                'title',
                'company__name',
                'column__title',
                'priority__title',
                'created_time',
                'owner__username',
                'board__name')
            for i in gret:
                ret = [i[j] for j in columns]
                objects.append(ret)
            filtered_count = all_records.filter(
                Q(title__icontains=global_search) |
                Q(company__name__icontains=global_search) |
                Q(column__title__icontains=global_search) |
                Q(board__name__icontains=global_search) |
                Q(owner__username__icontains=global_search) |
                Q(priority__title__icontains=global_search)
            ).count()
        else:
            # TODO: this same check is required in the other &_ajax views
            if all_records != 0:
                for i in all_records.order_by(order_direction + column)[start:start + length].values(
                        'id',
                        'title',
                        'company__name',
                        'column__title',
                        'priority__title',
                        'created_time',
                        'owner__username',
                        'board__name'):
                    ret = [i[j] for j in columns]
                    filtered_count = all_records.count()
                    objects.append(ret)
    else:
        filtered_count = 0
    # TODO: this same check is required in the other &_ajax views
    if not records_total:
        records_total = 0
    if not objects:
        objects = 0

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": filtered_count,
        "data": objects,
    })


def open_incidents_ajax(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    # Note: Ordering is implicit on created_time. If we we are passed a new ordering column,
    # it is not taken into account!
    # order_column = int(request.GET['order[0][column]'])
    # TODO: not quite sure how this is supposed to works or if it works
    order_direction = '' if request.GET['order[0][dir]'] == 'desc' else '-'
    # Since these are closed cards we have unanimously voted for ordering newest closed first
    column = 'created_time'
    backlog = Columntype.objects.all().filter(name="Backlog")
    global_search = request.GET['search[value]']
    # Note: If user != superuser we limit to company or owned/watched cards only!
    if request.user.profile_user.is_operator:
        records_total = Card.objects.all().filter(closed=False).filter(type="IN").filter(
            ~Q(column__usage__exact=backlog)
        ).count()
        all_records = Card.objects.all().filter(closed=False).filter(type="IN").filter(
            ~Q(column__usage__exact=backlog)
        ).distinct()
        if not all_records:
            all_records = 0

    # just for customer (NOT org admin)
    elif request.user.profile_user.is_customer and not request.user.profile_user.is_org_admin:
        all_records = Card.objects.all().filter(
            closed=False,
            type="IN").filter(
            watchers__id__exact=int(request.user.id)
        ).filter(
            ~Q(column__usage__exact=backlog)).distinct()
        records_total = all_records.count()
        if not all_records:
            all_records = 0



    # if we hit the else it means is_customer and org is_org_admin
    else:
        all_records = Card.objects.all().filter(closed=False, type="IN", company=request.user.profile_user.company.id).filter(
            ~Q(column__usage__exact=backlog)
        )
        records_total = all_records.count()
        if not all_records:
            all_records = 0

    # NOTE: not sure how this is supposed to work or if it works
    # columns = [i.name for i in Card._meta.get_fields()][1:]
    # I also know this is ugly, writing/hardcoding this 3 times like this.
    columns = ['id', 'title', 'company__name', 'column__title', 'created_time', 'owner__username', 'board__name']
    objects = []
    # search only if there are records otherwise dt throws alerts to the user
    if all_records != 0:
        if global_search:
            gret = all_records.filter(
                Q(title__icontains=global_search) |
                Q(company__name__icontains=global_search) |
                Q(owner__username__icontains=global_search) |
                Q(board__name__icontains=global_search) |
                Q(column__title__icontains=global_search)
            ).order_by(order_direction + column)[start:start + length].values(
                'id',
                'title',
                'company__name',
                'column__title',
                'created_time',
                'owner__username',
                'board__name')
            for i in gret:
                ret = [i[j] for j in columns]
                objects.append(ret)
            filtered_count = all_records.filter(
                Q(title__icontains=global_search) |
                Q(company__name__icontains=global_search) |
                ~Q(column__usage__exact=backlog) |
                Q(column__title__icontains=global_search)
            ).count()
        else:
            # TODO: this same check is required in the other &_ajax views
            if all_records != 0:
                for i in all_records.order_by(order_direction + column)[start:start + length].values(
                        'id',
                        'title',
                        'company__name',
                        'column__title',
                        'created_time',
                        'owner__username',
                        'board__name'):
                    ret = [i[j] for j in columns]
                    filtered_count = all_records.count()
                    objects.append(ret)
    else:
        filtered_count = 0
    # TODO: this same check is required in the other &_ajax views
    if not records_total:
        records_total = 0
    if not objects:
        objects = 0
    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": filtered_count,
        "data": objects,
    })


def overdue_cards_ajax(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    # Note: Ordering is implicit on created_time. If we we are passed a new ordering column,
    # it is not taken into account!
    # order_column = int(request.GET['order[0][column]'])
    # TODO: not quite sure how this is supposed to works or if it works
    order_direction = '' if request.GET['order[0][dir]'] == 'desc' else '-'
    # Since these are closed cards we have unanimously voted for ordering newest closed first
    column = 'created_time'
    backlog = Columntype.objects.all().filter(name="Backlog")
    global_search = request.GET['search[value]']
    # TODO: due dates are not inclusive of several hours
    # Note: If user != superuser we limit to company or owned/watched cards only!
    if request.user.profile_user.is_operator:
        all_records = Card.objects.filter(due_date__lte=today_date).filter(closed=False).filter(
            ~Q(column__usage__exact=backlog)
        ).distinct()
        total_count = all_records.count()
        if not all_records:
            all_records = 0

    # if we hit the else it means is_customer and/org is_org_admin
    else:
        all_records = Card.objects.all().filter(closed=True, company=request.user.profile_user.company.id).filter(
            ~Q(column__usage__exact=backlog)
        ).distinct()
        total_count = all_records.count()
        if not all_records:
            all_records = 0
    # NOTE: not sure how this is supposed to work or if it works
    # columns = [i.name for i in Card._meta.get_fields()][1:]
    # I also know this is ugly, writing/hardcoding this 3 times like this.
    columns = ['id', 'title', 'company__name', 'column__title', 'priority__title', 'created_time', 'owner__username', 'board__name']
    objects = []
    if all_records != 0:
        if global_search:
            gret = all_records.filter(
                Q(title__icontains=global_search) |
                Q(company__name__icontains=global_search) |
                Q(column__title__icontains=global_search) |
                Q(priority__title__icontains=global_search)|
                Q(owner__username__icontains=global_search)
            ).filter(~Q(column__usage__exact=backlog)).order_by(order_direction + column)[start:start + length].values(
                'id',
                'title',
                'company__name',
                'column__title',
                'priority__title',
                'created_time',
                'owner__username',
                'board__name')
            for i in gret:
                ret = [i[j] for j in columns]
                objects.append(ret)
            filtered_count = all_records.filter(
                Q(title__icontains=global_search) |
                Q(company__name__icontains=global_search) |
                Q(column__title__icontains=global_search) |
                Q(owner__username__icontains=global_search) |
                Q(priority__title__icontains=global_search)
            ).count()
        else:
            for i in all_records.order_by(order_direction + column)[start:start + length].values(
                    'id',
                    'title',
                    'company__name',
                    'column__title',
                    'priority__title',
                    'created_time',
                    'owner__username',
                    'board__name'):
                ret = [i[j] for j in columns]
                filtered_count = all_records.count()
                objects.append(ret)
    else:
        filtered_count = 0

    return JsonResponse({
        "sEcho": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "aaData": objects,
    })


def closed_cards_ajax(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    # Note: Ordering is implicit on created_time. If we we are passed a new ordering column,
    # it is not taken into account!
    # order_column = int(request.GET['order[0][column]'])
    # TODO: not quite sure how this is supposed to works or if it works
    order_direction = '' if request.GET['order[0][dir]'] == 'desc' else '-'
    # Since these are closed cards we have unanimously voted for ordering newest closed first
    column = 'created_time'
    backlog = Columntype.objects.all().filter(name="Backlog")
    global_search = request.GET['search[value]']
    # NOTE: not sure how this is supposed to work or if it works
    # columns = [i.name for i in Card._meta.get_fields()][1:]
    # I also know this is ugly, writing/hardcoding this 3 times like this.
    columns = ['id', 'title', 'company__name', 'priority__title', 'created_time', 'owner__username', 'board__name']

    # NOTE order is important here. superuser will almost always have is_operator so check this first.
    # is_perator has more privs than is_customer ...
    if request.user.is_superuser:
        all_records = Card.objects.all().filter(closed=True).filter(
            ~Q(column__usage__exact=backlog)
        ).distinct()
        total_count = all_records.count()
        if not all_records:
            all_records = 0
    elif request.user.profile_user.is_operator:
        all_records = Card.objects.filter(
            closed=True).filter(
            Q(owner=request.user) |
            ~Q(column__usage__exact=backlog) |
            Q(watchers__id__exact=request.user.id)).distinct()
        total_count = all_records.count()
        if not all_records:
            all_records = 0
    # Note: If users != operator we limit to company
    # if we hit the else it means is_customer
    else:
        # if no company
        try:
            company = request.user.profile_user.company.id
        except:
            company = None
        if company:
            all_records = Card.objects.all().filter(
                Q(watchers__in=[request.user]) | Q(company=request.user.profile_user.company.id)
                ).filter(closed=True).distinct()
            total_count = all_records.count()
            if not all_records:
                all_records = 0
        else:
            all_records = Card.objects.all().filter(
                Q(watchers__in=[request.user])
            ).filter(closed=True).distinct()
            total_count = all_records.count()
            if not all_records:
                all_records = 0
    objects = []
    if all_records != 0:
        if global_search:
            gret = all_records.filter(
                Q(title__icontains=global_search) |
                Q(company__name__icontains=global_search) |
                Q(column__title__icontains=global_search) |
                Q(owner__username__icontains=global_search) |
                Q(priority__title__icontains=global_search)
            ).order_by(order_direction + column)[start:start + length].values(
                'id',
                'title',
                'company__name',
                'priority__title',
                'created_time',
                'owner__username',
                'board__name')
            for i in gret:
                ret = [i[j] for j in columns]
                objects.append(ret)
            filtered_count = all_records.filter(
                Q(title__icontains=global_search) |
                Q(company__name__icontains=global_search) |
                Q(column__title__icontains=global_search) |
                ~Q(column__usage__exact=backlog) |
                Q(priority__title__icontains=global_search)
            ).count()
        else:
            for i in all_records.order_by(order_direction + column)[start:start + length].values(
                    'id',
                    'title',
                    'company__name',
                    'priority__title',
                    'created_time',
                    'owner__username',
                    'board__name'):
                ret = [i[j] for j in columns]
                filtered_count = all_records.count()
                objects.append(ret)
    else:
        filtered_count = 0

    return JsonResponse({
        "sEcho": draw,
        "iTotalRecords": total_count,
        "iTotalDisplayRecords": filtered_count,
        "aaData": objects,
    })


# TODO: parameterize this to get template based on what we're trying to view:
# weekly report, reminders, etc
@login_required
@staff_member_required
def emailviewer(request):
    """ View for the user Profile page."""
    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    # TODO: check permissions to view?

    seven_days_from_now = datetime.now() + timedelta(days=7)
    past_seven_days = datetime.now() - timedelta(days=7)
    today_date = datetime.now()

    overdueCards = Card.objects.filter(due_date__lt=today_date).filter(closed=False).filter(owner=u).count()
    overdue_in_seven = Card.objects.filter(due_date__gte=today_date, due_date__lte=seven_days_from_now).filter(owner=u).filter(
        closed=False).count()
    closed = Card.objects.filter(closed=True).filter(modified_time__range=[past_seven_days, today_date]).filter(owner=u).count()

    context_dict = {
        'user': u,
        'overdueCards': overdueCards,
        'overdue_in_seven': overdue_in_seven,
        'closed': closed,
    }

    return render_to_response('emails/weeklydashboardreport.html', context_dict, context)


@login_required
@staff_member_required
def getCardsCreatedToday(request):
    context = RequestContext(request)
    if request.is_ajax() or request.method == 'GET':
        try:
            cards = Card.objects.all().filter(created_time__gte=today_date)
            results = [cards.count()]
        except ObjectDoesNotExist:
            results = 0
        data = json.dumps(results)
    return HttpResponse(data, content_type='application/json')


@login_required
@staff_member_required
def getWlogsCreatedToday(request):
    context = RequestContext(request)
    if request.is_ajax() or request.method == 'GET':
        try:
            results = Worklog.objects.filter(created_time__gte=today_date).all().filter(owner=request.user).count()
        except ObjectDoesNotExist:
            results = 0
        data = json.dumps(results)
    return HttpResponse(data, content_type='application/json')

@login_required
@staff_member_required
def getTodaysTasks(request):
    if request.is_ajax() or request.method == 'GET':
        try:
            results = Task.objects.filter(created_time__gte=today_date).all().filter(owner=request.user).count()
        except ObjectDoesNotExist:
            results = 0
        data = json.dumps(results)
    return HttpResponse(data, content_type='application/json')


@login_required
def profile(request):
    """ View for the user Profile page."""
    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    boards = Board.objects.filter(archived=False)
    if request.user.profile_user.is_customer:
        userform = EditUserForm(
            initial={
                'username': request.user,
                'email': request.user.email,

            }
        )
        userprofileform = EditCustomerProfileForm(
            initial={
                'picture': request.user.profile_user.picture,
                'company': request.user.profile_user.company,


            }
        )
        context_dict = {
            'site_title': "Profile | Spearhead Systems",
            'page_name': "Profile",
            'user': u,
            'userprofile': up,
            'doitVersion': doitVersion,
            'userform': userform,
            'userprofileform': userprofileform,
        }
    elif request.user.profile_user.is_org_admin:
        userform = EditUserForm(
            initial={
                'username': request.user,
                'email': request.user.email,

            }
        )
        userprofileform = EditCustomerProfileForm(
            initial={
                'picture': request.user.profile_user.picture,
                'company': request.user.profile_user.company,

            }
        )
        context_dict = {
            'site_title': "Profile | Spearhead Systems",
            'page_name': "Profile",
            'user': u,
            'userprofile': up,
            'doitVersion': doitVersion,
            'userform': userform,
            'userprofileform': userprofileform,
            'boards': boards,
        }
    elif request.user.profile_user.is_operator:
        userform = EditUserForm(
            initial={
                'username': request.user,
                'email': request.user.email,

            }
        )
        userprofileform = EditCustomerProfileForm(
            initial={
                'picture': request.user.profile_user.picture,
                'company': request.user.profile_user.company,

            }
        )
        context_dict = {
            'site_title': "Profile | Spearhead Systems",
            'page_name': "Profile",
            'user': u,
            'userprofile': up,
            'doitVersion': doitVersion,
            'userform': userform,
            'userprofileform': userprofileform,
            'boards': boards,
        }
    elif request.user.profile_user.is_superuser:
        userform = EditUserForm(
            initial={
                'username': request.user,
                'email': request.user.email,

            }
        )
        userprofileform = EditCustomerProfileForm(
            initial={
                'picture': request.user.profile_user.picture,
                'company': request.user.profile_user.company,

            }
        )
        context_dict = {
            'site_title': "Profile | Spearhead Systems",
            'page_name': "Profile",
            'user': u,
            'userprofile': up,
            'doitVersion': doitVersion,
            'userform': userform,
            'userprofileform': userprofileform,
            'boards': boards,
        }

    return render(request, 'profile.html', context_dict)
