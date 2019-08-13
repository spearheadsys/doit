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
from datetime import date, timedelta
from card.models import Worklog
from contact.models import UserProfile
# verions
from django.conf import settings
import json
from dal import autocomplete
from organization.models import EmailDomain
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
    current_url = resolve(request.path_info).url_name
    org_list = Organization.objects.all().filter(active=True)
    # for i in org_list:
    #     print i
    # contract_list = Contract.objects.all().filter(active=True)
    user_list = [active_user for active_user in UserProfile.objects.select_related().all()
                 if active_user.user.is_active]

    addOrganizationForm = AddOrganizationsForm()

    # worked hours this month
    today_date = date.today()
    #TODO - get the compant id we want here
    this_month_minutes = Worklog.objects.all().filter(
        created_time__month=today_date.month,
        card__company=1
    )

    context_dict = {
        'site_title': "Organizations | Spearhead Systems",
        'page_name': "Organizations",
        'addOrganizationForm': addOrganizationForm,
        'active_url': current_url,
        'site_description': "",
        'org_list': org_list,
        # 'contract_list': contract_list,
        'user_list': user_list,
        'doitVersion': doitVersion,
    }
    return render(request, 'organizations.html', context_dict)


@login_required
def change_organization(request):
    # >>> for i in orgs:
    # ...     cards_count = Card.objects.all().filter(closed=False, company=i).count()
    # ...     print(cards_count, i)
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