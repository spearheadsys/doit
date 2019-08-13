from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import resolve
from django.template import RequestContext
from django.shortcuts import render_to_response
# user auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from contract.models import Contract
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from contract.forms import ContractForm
from organization.models import Organization

# Create your views here.
@login_required
def contracts(request):
    """ """
    if request.user.profile_user.is_customer:
        return HttpResponse("You do not have permissions to view this page.")
    # current_url = resolve(request.path_info).url_name
    contracts_list = Contract.objects.all()
    context = RequestContext(request)
    context_dict = {
        'page_name': "Contracts",
        'contracts_list': contracts_list,
    }
    return render_to_response('contracts/contracts.html', context_dict, context)

@login_required
@staff_member_required
def addcontract(request, company=None):
    """ """
    if request.user.profile_user.is_customer:
        return HttpResponse("You do not have permissions to view this page.")
    # u = User.objects.get(username=request.user)
    # If the form has been submitted...
    if request.is_ajax() or request.method == 'POST':
        contract_form = ContractForm(request.POST)
        # contract_form = request.POST['title']
        if contract_form.is_valid():
            contract_form.save()
            return HttpResponseRedirect('/contracts/')
        
        # TODO: add tracker (created contract, etc.)
        # CARD CREATED TRACKER
        # ctype = ContentType.objects.get_for_model(card_created)
        # tracker = Tracker.objects.create(
        #     created_time=datetime.now(),
        #     content_type=ctype,
        #     object_id=card_created.id,
        #     action=" created the card ",
        #     updated_fields=(' on board ') + str(
        #         card_created.board.name) + str(' and column ') + str(
        #         card_created.column.title),
        #     owner=u,
        # )
        # tracker.save()
        # END CARD CREATED TRACKER
        return HttpResponseRedirect('/contracts/')
    else:
        # display addcontract page
        if company:
            instance = Organization.objects.get(id=company)
            add_contract_form = ContractForm(
                initial={
                    'company': company,
                }
            )
        else:
            add_contract_form = ContractForm()
        context_dict = {
            'site_title': "Contracts | Spearhead Systems",
            'page_name': "Add a Contract",
            'add_contract_form': add_contract_form,
        }
        return render(request, 'contracts/addcontract.html', context_dict)
    # not very helpful TODO something
    # return render(request, 'cards/addcard.html', context_dict)

def editcontract(request, contract=None):
    """ """
    instance = Contract.objects.get(id=contract)
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # EDIT CONTRACT TRACKER
            # TODO: get this working
            # eureka (changed_data att of forms!)
            # ctype = ContentType.objects.get_for_model(instance)
            # tracker = Tracker.objects.create(
            #     created_time=datetime.now(),
            #     content_type=ctype,
            #     object_id=instance.id,
            #     updated_fields=str(" updated ") + str(form.changed_data),
            #     owner=request.user,
            #     action=action_text
            # )
            # tracker.save()
            # END EDIT CONTRACT TRACKER
        return HttpResponseRedirect('/contracts/')
    else:
        contract = Contract.objects.get(id=contract)
        add_contract_form = ContractForm(instance=instance)
        context_dict = {
            'site_title': "Contracts | Spearhead Systems",
            'page_name': "Edit a Contract",
            'add_contract_form': add_contract_form,
            'contract': contract,
        }
        # return render_to_response(
        #     'cards/editcard.html', context_dict, context)
        return render(request, 'contracts/editcontract.html', context_dict)

def deletecontract(request, contract=None):
    """ Deletes a contract instance. """
    instance = Contract.objects.get(id=contract)
    instance.delete()
    return HttpResponseRedirect('/contracts/')
