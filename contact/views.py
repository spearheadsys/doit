from django.http import HttpResponseRedirect, HttpResponse
from django.urls import resolve
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from contact.forms import ContactForm, UserProfileForm
from doit.forms import EditCustomerProfileForm
from organization.models import Organization
from django.shortcuts import render
from contact.models import UserProfile
from board.models import Board
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.
@login_required
def contacts(request, company=None):
    """ Contacts view."""
    add_contact_form = ContactForm()
    # If the form has been submitted...
    if request.is_ajax() or request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return HttpResponseRedirect('/contacts/')
        
        # TODO: add tracker (created contact, etc.)
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
        return HttpResponseRedirect('/contacts/')
    else:
        # display addcontact page
        if company:
            instance = Organization.objects.get(id=company)
            add_contact_form = ContactForm(
                initial={
                    'company': company,
                }
            )
        else:
            contacts_list = UserProfile.objects.all().filter(is_customer=True)
            boards = Board.objects.filter(archived=False)
            context_dict = {
                'site_title': "Contacts | Spearhead Systems",
                'page_name': "Add a Contact",
                'add_contact_form': add_contact_form,
                'contacts_list': contacts_list,
                'boards': boards,
            }
    return render(request, 'contacts/contacts.html', context_dict)
    # return render(request, 'contacts/contacts.html', context_dict)


def addcontact(request, company=None):
    """ Add a contact to an organization. """
    # If the form has been submitted...
    if request.is_ajax() or request.method == 'POST':
        contact_form = ContactForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)

        if contact_form.is_valid() and userprofile_form.is_valid():
            user = contact_form.save()
            user.set_password(user.password)
            user.save()

            profile = userprofile_form.save(commit=False)
            profile.user = user
            profile.is_customer = True

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
        else:
            # print contact_form.errors, userprofile_form.errors
            # TODO: print useful message to user and redirect back to addcontact 
            return HttpResponseRedirect('/contacts/')
        
        # TODO: add tracker (created contact, etc.)
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

        # user was added
        return HttpResponseRedirect('/contacts/')
    else:
        # display addcontact page with company preselected
        if company:
            # TODO: intitial company is not picking up!!
            instance = Organization.objects.get(id=company)
            add_contact_form = ContactForm(
                initial={
                    'company': company,
                }
            )
            add_userprofile_form = UserProfileForm()
        else:
            add_contact_form = ContactForm()
            add_userprofile_form = UserProfileForm()
        boards = Board.objects.filter(archived=False)
        context_dict = {
            'site_title': "Contacts | Spearhead Systems",
            'page_name': "Add a Contact",
            'add_contact_form': add_contact_form,
            'add_userprofile_form': add_userprofile_form,
            'boards': boards,
        }
    return render(request, 'contacts/addcontact.html', context_dict)
    # not very helpful TODO something
    # return render(request, 'cards/addcard.html', context_dict)


def editcontact(request, contact=None):
    """ """
    instance = User.objects.get(id=contact)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # EDIT CONTACT TRACKER
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
            # END EDIT CONTACT TRACKER
        return HttpResponseRedirect('/contacts/')
    else:
        contact = User.objects.get(id=contact)
        add_contact_form = ContactForm(instance=instance)
        profile_instance = UserProfile.objects.get(user=instance)
        add_userprofile_form = UserProfileForm(instance=profile_instance)
        boards = Board.objects.filter(archived=False)
        context_dict = {
            'site_title': "Contacts | Spearhead Systems",
            'page_name': "Edit a Contact",
            'add_contact_form': add_contact_form,
            'add_userprofile_form': add_userprofile_form,
            'contact': contact,
            'boards': boards,
        }
        return render(request, 'contacts/editcontact.html', context_dict)


def deletecontact(request, contact=None):
    """ Deletes a contact instance. """
    # todo talk about the differing ids in template and what were doing here
    profile = UserProfile.objects.get(id=contact)
    user = User.objects.get(id=profile.user.id)
    # print profile.id
    profile.delete()
    user.delete()
    return HttpResponseRedirect('/contacts/')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return render(request,'profile/pass_ok.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/change_password.html', {
        'form': form
    })

def change_picture(request, contact=None):
    """ """
    instance = User.objects.get(id=contact)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # EDIT CONTACT TRACKER
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
            # END EDIT CONTACT TRACKER
        return HttpResponseRedirect('/contacts/')
    else:
        contact = User.objects.get(id=contact)
        add_contact_form = ContactForm(instance=instance)
        profile_instance = UserProfile.objects.get(user=instance)
        add_userprofile_form = UserProfileForm(instance=profile_instance)
        boards = Board.objects.filter(archived=False)
        context_dict = {
            'site_title': "Contacts | Spearhead Systems",
            'page_name': "Edit a Contact",
            'add_contact_form': add_contact_form,
            'add_userprofile_form': add_userprofile_form,
            'contact': contact,
            'boards': boards,
        }
        return render(request, 'contacts/editcontact.html', context_dict)