from django.http import HttpResponse, HttpResponseRedirect
# from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from card.models import Card
from comment.models import Comment
from contact.models import UserProfile
from attachment.models import Attachment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# testing
import os
from django.conf import settings

#  TODO: add tracker for attachments

@login_required
def attachments(request):
    # context = RequestContext(request)
    context_dict = {
        'site_title': "Attachments 404 | Spearhead Systems",
        'page_name': "Attachments 404",
    }
    u = User.objects.get(username=request.user)
    up = u.profile_user

    if up.is_customer:
        return HttpResponse("You do not have permissions to view this page.")
    # return render_to_response('attachments/null.html', context_dict, context)
    return render(request, 'attachments/null.html', context_dict)


@login_required
@csrf_exempt
def addattachments(request):
    u = User.objects.get(username=request.user)
    up = u.profile_user
    if request.is_ajax() or request.method == 'POST':
        card = request.POST['card']
        related_card = Card.objects.get(id=card)
        for filename, uploaded_file in request.FILES.iteritems():
            f = uploaded_file.content_type
            if up.is_customer:
                if u.profile_user.company == related_card.company:
                    if u.profile_user.is_org_admin or u in related_card.watchers.all():
                        dirspath = 'uploads/{}/{}'.format(related_card.board.id, related_card.id)
                        path = 'uploads/{}/{}/{}'.format(related_card.board.id, related_card.id, uploaded_file)
                        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, dirspath)):
                            os.makedirs(os.path.join(settings.MEDIA_ROOT, dirspath))
                        new_up_path = os.path.join(settings.MEDIA_ROOT, path)
                        print("CUSTOMER PATH is >>> ", new_up_path)
                        print("CUSTOMER FILENAME is >>> ", uploaded_file)
                        destination = open(new_up_path, 'wb+')
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
                        destination.close()
                        new_attachment = Attachment.objects.create(
                            name=uploaded_file.name,
                            content=uploaded_file,
                            uploaded_by=u,
                            card=related_card,
                            mimetype=f,
                        )
                        data = {
                            'name': new_attachment.name,
                            'url': str(new_attachment)
                        }
                        dump = json.dumps(data)
                        return HttpResponse(dump, content_type='application/json')
                return HttpResponse("You do not have permissions to view this page.")
            # # write file to upload dir
            ## TODO: check if file already exista otherwise we truncate and this
            # is probably NOT what we want
            dirspath = 'uploads/{}/{}'.format(related_card.board.id, related_card.id)
            path = 'uploads/{}/{}/{}'.format(related_card.board.id, related_card.id, uploaded_file)
            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, dirspath)):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, dirspath))
            new_up_path = os.path.join(settings.MEDIA_ROOT, path)
            print("NEW UP PATH is >>> ", new_up_path)
            print("FILENAME is >>> ", uploaded_file)
            destination = open(new_up_path, 'wb+')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()
            print("PATH is >>> ", path)
            # end write
            # TODO: clean files, make sure we do not bad things
            new_attachment = Attachment.objects.create(
                name=uploaded_file.name,
                content=path,
                uploaded_by=u,
                card=related_card,
                mimetype=f,
            )
            data = {
                'name': new_attachment.name,
                'url': str(new_attachment)
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')
        else:
            print request
            # not sure how you got here ..
            # return render_to_response('attachments/null.html')
            return JsonResponse({'status': '500'})


@login_required
def get_attachments(request):
    # context = RequestContext(request)
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('card', '')
        if not q:
            return HttpResponse("This feature is not enabled.")
        card = Card.objects.get(id=q)
        ctype = ContentType.objects.get_for_model(card)
        attachments = Attachment.objects.filter(
            card_id=card.id
        )
        results = []
        for co in attachments:
            co_json = {}
            co_json['id'] = co.id
            co_json['attachment'] = str(co)
            co_json['name'] = co.name
            co_json['mimetype'] = co.mimetype
            results.append(co_json)
        data = json.dumps(results)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponse("This feature is not enabled.")

