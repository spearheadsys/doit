from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import resolve
from django.template import RequestContext
from django.shortcuts import render_to_response, render
# user auth
from django.contrib.auth.decorators import login_required, user_passes_test
# login
from django.contrib.auth.models import User
from forms import AddOrganizationsForm
from organization.models import Organization
from comment.models import Comment
from datetime import date, timedelta
from card.models import Worklog, Card
from contact.models import UserProfile
from django.contrib.contenttypes.models import ContentType
# verions
from django.conf import settings
import json
from dal import autocomplete
from board.models import Board
from organization.models import EmailDomain
import collections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

doitVersion = settings.DOIT_VERSION




class EmailDomainAutocomplete(autocomplete.Select2QuerySetView):
    # TODO: secure/restrict things accordingly
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return EmailDomain.objects.none()

        qs = EmailDomain.objects.all()

        if self.q:
            qs = qs.filter(domain__icontains=self.q)

        return qs


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
        'addOrganizationForm': addOrganizationForm,
        # 'active_url': current_url,
        'site_description': "",
        # 'org_list': org_list,
        'companies': companies,
        # 'user_list': user_list,
        'doitVersion': doitVersion,
        'boards': boards,
    }
    return render(request, 'organizations.html', context_dict)


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
            print form.errors
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
            'site_description': "",
        }
        return render_to_response('cases/addorganization.html', context_dict, context)

@login_required
def add_organization(request):
    """ Add an Organization object."""
    current_url = resolve(request.path_info).url_name
    if request.is_ajax() or request.method == 'POST':
        form = AddOrganizationsForm(request.POST)
        if form.is_valid():
            # add card to database
            model_instance = form.save(commit=True)
            model_instance = form.save()
            return HttpResponseRedirect('/organizations/')
        else:
            print form.errors
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
            'site_description': "",
        }
        return render_to_response('cases/addorganization.html', context_dict, context)


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
    return HttpResponseRedirect('/organizations/')


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