from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from card.models import Card
from contact.models import UserProfile
from comment.models import Comment
from organization.models import Organization
from django.conf import settings
from datetime import datetime, time, timedelta
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from board.models import Board
from django.db.models import Q


# GLOBALS
doitVersion = settings.DOIT_VERSION
today_date = datetime.today()


# Create your views here.
@login_required
@csrf_exempt
def reports(request):
    u = User.objects.get(username=request.user)
    up = u.profile_user

    if not up.is_superuser:
        return HttpResponse("This feature is not enabled.")
    # try:
    #     up = UserProfile.objects.get(user=u)
    # except:
    #     up = None
    allCards = Card.objects.all()
    organizations = Organization.objects.all()
    boards = Board.objects.filter(archived=False)
    reportusers = User.objects.all().filter(is_staff=True)
    all_operators = UserProfile.objects.all().filter(user__is_active=True, is_operator=True)
    # todo add caching here
    cards_per_operator = {}
    closed_cards_per_operator = {}
    time_worked_per_operator = {}
    for operator in all_operators:
        cards_per_operator[operator] = Card.objects.all().filter(closed=False, owner=operator.user.id).filter(~Q(column__title="Backlog")).count()
    for operator in all_operators:
        closed_cards_per_operator[operator] = Card.objects.all().filter(closed=True, owner=operator.user.id).count()
    for operator in all_operators:
        time_worked_per_operator[operator] = Comment.objects.all().filter(owner=operator.user.id).aggregate(minutes=Sum('minutes'))
    # end caching here

    if request.method == "POST":
        organization = request.POST['organization'] or None
        reportperiod = request.POST['daterange'] or None
        reportuser = request.POST['user'] or None
        start, stop = reportperiod.split(' - ', 1)
        startperiod = (datetime.strptime(start, '%Y-%m-%d %H:%M'))
        stopperiod = (datetime.strptime(stop, '%Y-%m-%d  %H:%M') + timedelta(days=1))

        # TODO: analytics.html it does not make sense to select both user and company
        # or does it? whichvever the case may be this is not possible yet.
        # just daterange
        if not organization and not reportuser:
            reportresult = Comment.objects.prefetch_related().filter(
                created_time__range=(startperiod, stopperiod)
            ).filter(minutes__gt=0)
        # owner
        elif not organization and reportuser:
            reportresult = Comment.objects.prefetch_related().filter(
                created_time__range=(startperiod, stopperiod)
            ).filter(owner=reportuser).filter(minutes__gt=0)

        # company
        elif organization:
            company = Organization.objects.get(id=organization)
            print("company >>> ", company, company.id)
            tempreportresult = Comment.objects.prefetch_related().filter(
                created_time__range=(startperiod, stopperiod)
            ).filter(minutes__gt=0)
            to_remove = []
            for i in tempreportresult:
                if Card.objects.get(id=i.object_id).company.id != company.id:
                    to_remove.append(i.id)
            reportresult = tempreportresult.exclude(id__in=to_remove)
        else:
            reportresult = Comment.objects.prefetch_related().filter(
                created_time__range=(startperiod, stopperiod)
            ).filter(minutes__gt=0)

        totalminutes = reportresult.aggregate(Sum('minutes'))
        nonbillable = reportresult.filter(billable=False).aggregate(Sum('minutes'))
        totalworkingminutes = reportresult.filter(overtime=False).aggregate(Sum('minutes'))
        totalovertimeminutes = reportresult.filter(overtime=True).aggregate(Sum('minutes'))
        # generate one time analytics
        context_dict = {
            'site_title': "Reports | Spearhead Systems",
            'page_name': "Reports",
            'doitVersion': doitVersion,
            'allCards': allCards,
            'organization': organization,
            'organizations': organizations,
            'reportusers': reportusers,
            'reportresult': reportresult,
            'reportperiod': reportperiod,
            'totalminutes': totalminutes,
            'totalworkingminutes': totalworkingminutes,
            'totalovertimeminutes': totalovertimeminutes,
            'nonbillable': nonbillable,
            'boards': boards,
            'cards_per_operator': cards_per_operator,
            'closed_cards_per_operator': closed_cards_per_operator,
            'time_worked_per_operator': time_worked_per_operator,
        }
        return render(request, 'analytics/analytics.html', context_dict)

    else:
        context_dict = {
            'site_title': "Reports | Spearhead Systems",
            'page_name': "Reports",
            'doitVersion': doitVersion,
            'allCards': allCards,
            'organizations': organizations,
            'cards_per_operator': cards_per_operator,
            'closed_cards_per_operator': closed_cards_per_operator,
            'time_worked_per_operator': time_worked_per_operator,
            'boards': boards,
        }
        return render(request, 'analytics/analytics.html', context_dict)

