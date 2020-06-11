from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from card.models import Worklog, Card, Task
from comment.models import Comment
from organization.models import Organization
from django.conf import settings
from datetime import datetime, time, timedelta
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from board.models import Board


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
    allTasks = Task.objects.all()
    organizations = Organization.objects.all()
    boards = Board.objects.filter(archived=False)
    reportusers = User.objects.all().filter(is_staff=True)
    if request.method == "POST":
        organization = request.POST['organization'] or None
        reportperiod = request.POST['daterange'] or None
        reportuser = request.POST['user'] or None
        if reportperiod:
            start, stop = reportperiod.split(' - ', 1)
        startperiod = (datetime.strptime(start, '%Y-%m-%d %H:%M'))
        stopperiod = (datetime.strptime(stop, '%Y-%m-%d  %H:%M') + timedelta(days=1))
        reportresult = Comment.objects.prefetch_related().filter(
            created_time__range=(startperiod, stopperiod)
        ).filter(minutes__gt=0)
        totalminutes = reportresult.aggregate(Sum('minutes'))
        nonbillable = reportresult.filter(billable=False).aggregate(Sum('minutes'))
        totalworkingminutes = reportresult.filter(overtime=False).aggregate(Sum('minutes'))
        totalovertimeminutes = reportresult.filter(overtime=True).aggregate(Sum('minutes'))
        # generate one time report
        context_dict = {
            'site_title': "Reports | Spearhead Systems",
            'page_name': "Reports",
            'doitVersion': doitVersion,
            'allCards': allCards,
            'allTasks': allTasks.count(),
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
        }
        return render(request, 'report/reports.html', context_dict)

    else:
        context_dict = {
            'site_title': "Reports | Spearhead Systems",
            'page_name': "Reports",
            'doitVersion': doitVersion,
            'allCards': allCards,
            'allTasks': allTasks.count(),
            'organizations': organizations,
            'reportusers': reportusers,
            'boards': boards,
        }
        return render(request, 'report/reports.html', context_dict)

