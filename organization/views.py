from django.http import HttpResponseRedirect, HttpResponse
from django.urls import resolve
from django.template import RequestContext
from django.shortcuts import render
# user auth
from django.contrib.auth.decorators import login_required
# login
from django.contrib.auth.models import User
from organization.forms import AddOrganizationsForm
from organization.models import Organization, KnowledgeBase, KnowledgeBaseCategory, \
    KnowledgeBaseArticle
from card.models import Worklog, Card
from contact.models import UserProfile
# verions
from django.conf import settings
import json
from board.models import Board
from django.http import JsonResponse
from django.db.models import Q
import collections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

SITE_URL = settings.SITE_URL
doitVersion = settings.DOIT_VERSION


@login_required
# @user_passes_test(lambda u: u.is_superuser)
# Create your views here.
def organizations(request):

    if request.user.profile_user.is_customer:
        return HttpResponse("You do not have permissions to view this page.")
    # current_url = resolve(request.path_info).url_name
    org_list = Organization.objects.all().filter(active=True).order_by('name')
    # user_list = [active_user for active_user in UserProfile.objects.select_related().all()
    #              if active_user.user.is_active]
    boards = Board.objects.filter(archived=False)
    addOrganizationForm = AddOrganizationsForm()
    companiesdict = collections.OrderedDict()
    for company in org_list:
        companiesdict[company] = {'contacts': UserProfile.objects.filter(company=company),
                              'open_cards': Card.objects.filter(company=company, closed=False).count(),
                              'closed_cards': Card.objects.filter(company=company, closed=True).count()}

    # TODO: lazy load orgs in paginated mannger

    p = Paginator(tuple(companiesdict.items()), 20)
    page = request.GET.get('page', 1)

    try:
        companies = p.page(page)
    except PageNotAnInteger:
        companies = p.page('page')
    except EmptyPage:
        companies = p.page(p.num_pages)

    context_dict = {
        'site_title': "Organizations | DoIT Spearhead Systems",
        'page_name': "Organizations",
        'addOrganizationForm': addOrganizationForm,
        # 'active_url': current_url,
        # 'org_list': org_list,
        'companies': companies,
        # 'user_list': user_list,
        'doitVersion': doitVersion,
        'boards': boards,
        'SITE_URL': SITE_URL,
    }
    return render(request, 'organization/organizations.html', context_dict)


@login_required
def all_companies_dt(request):
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])

    # Note: Ordering is implicit on created_time. If we we are passed a new ordering column,
    # it is not taken into account!
    # order_column = int(request.GET['order[0][column]'])
    # TODO: not quite sure how this is supposed to works or if it works
    order_direction = ''
    global_search = request.GET['search[value]']
    column = 'id'
    # Note: If user != superuser we limit to company or owned/watched cards only!
    if request.user.profile_user.is_operator:
        all_records = Organization.objects.all()
        records_total = all_records.count()
        if not all_records:
            all_records = 0

    # if user selects all (-1 in datatables) we need to figure out our length here
    if length < 0:
        length = all_records.count()
    columns = ['id', 'name']
    objects = []
    if all_records != 0:
        if global_search:
            grep = all_records.filter(
                Q(name__icontains=global_search)
            ).order_by(order_direction + column )[start:start + length].values(
                'id',
                'name')
            for i in grep:
                ret = [i[j] for j in columns]
                objects.append(ret)
            filtered_count = all_records.filter(
                Q(name__icontains=global_search)
            ).count()
        else:
            # TODO: this same check is required in the other &_ajax views
            if all_records != 0 or all_records < 0:
                for i in all_records.order_by(order_direction + column)[start:start + length].values(
                        'id',
                        'name'):
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


@login_required
def change_organization(request):
    current_url = resolve(request.path_info).url_name
    if request.is_ajax() or request.method == 'POST':
        form = AddOrganizationsForm(request.POST)
        if form.is_valid():
            # add card to database
            model_instance = form.save(commit=True)
            model_instance = form.save()
            return HttpResponseRedirect('/organizations/')
        else:
            print(form.errors)
        return HttpResponseRedirect('/organizations/')
    else:
        u = User.objects.get(username=request.user)
        addOrganizationForm = AddOrganizationsForm(
            #todo : figure why this is not autopopulated
            initial={
                'owner': u.id,
            }
        )
        context = RequestContext(request)
        context_dict = {
            'site_title': "Cases | Spearhead Systems",
            'addOrganizationForm': addOrganizationForm,
            'page_name': "Add Organization",
            'active_url': current_url,
        }
        # return render_to_response('cases/addorganization.html', context_dict, context)
        return render(request, 'cases/addorganization.html', context_dict)


def delete_organization(request, company=None):
    """ Delete an Organization object."""
    # who can delete organization? Just superusers!
    if request.user.profile_user.is_superuser:
        organization = Organization.objects.get(id=company)
        # delete all organization contacts
        for i in UserProfile.objects.filter(company=company):
            user = User.objects.get(id=i.user.id)
            user.delete()
            i.delete()
        # delete comments
        cards = Card.objects.filter(company=company)
        for i in cards:
            i.delete()
        # delete the org last because we need the card m2m reverse to ge the comments
        organization.delete()
    return HttpResponse("200 ok", content_type='application/json')


@login_required
# get company view
def get_company(request):
    """ Get a Company object from ajax search. """
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('q', '')
        company = Organization.objects.filter(name__icontains=q)[:20]
        results = []
        for co in company:
            co_json = {}
            co_json['id'] = co.id
            co_json['name'] = co.name
            # co_json['value'] = co.id  # in the form we actually need this
            # value to submit but would like to show
            # the name in the view and not the ID!!
            results.append(co_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    # mimetype = 'application/json'
    return HttpResponse(data, content_type='application/json')


def kblist(request, company=None):
    try:
        company = Organization.objects.get(id=company)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/organizations')

    # get all knowledge bases for this company
    kbs = KnowledgeBase.objects.all().filter(company=company)
    categories = KnowledgeBaseCategory.objects.all().filter(company=company)
    kbarticles = KnowledgeBaseArticle.objects.all().filter(knowledgebase__company=company)


    context_dict = {
        # 'site_title': "Knowledge bases | DoIT Spearhead Systems",
        'site_title': f"KB's {company} | DoIT Spearhead Systems",
        'page_name': "KBs",
        'kbs': kbs,
        'kbarticles': kbarticles,
        'company': company,
        'categories': categories,
        'SITE_URL': SITE_URL,
    }
    return render(request, 'organization/kblist.html', context_dict)


def editkb(request, kb=None):
    try:
        kb = KnowledgeBaseArticle.objects.get(id=kb)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/kbs')



    context_dict = {
        # 'site_title': "Knowledge bases | DoIT Spearhead Systems",
        'site_title': f"Edit KB {kb} | DoIT Spearhead Systems",
        'page_name': f"{kb}",
        'kb': kb,

        'SITE_URL': SITE_URL,
    }
    return render(request, 'organization/editkb.html', context_dict)