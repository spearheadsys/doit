from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.http import JsonResponse
from django.contrib.auth.models import User
from contact.models import UserProfile
from comment.models import Comment
from card.models import Card, Column, Columntype
from doit.models import Tracker
from datetime import date, datetime
# user auth
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
import json
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from django.conf import settings

doit_myemail = settings.DOIT_MYEMAIL


@login_required
@csrf_exempt
def add_comment(request):
    if request.is_ajax() or request.method == 'POST':
        comment_form = request.POST['comment']
        # TODO: if the comment form is submitted but the comment
        # text is empty it still ends up here only to die when
        # addnig ctype tracker (comment_object). either solve it here
        # or in the UI
        card = request.POST['card']
        minutes = request.POST.get('minutes', '0')
        if minutes == '':
            minutes = 0
        overtime = request.POST.get('overtime', False)
        billable = request.POST.get('billable', False)
        internal = request.POST.get('internal', False)
        public = request.POST.get('public', False)
        public_close = request.POST.get('public_close', False)
        if public is not False:
            public = True
        if public_close is not False:
            public_close = True
        if billable is not False:
            billable = True
        if overtime is not False:
            overtime = True
        userid = request.user
        # TODO: make sure user has permission to add this comment
        # by looking at watchers, company with is_org_admin
        if request.user.profile_user.is_customer:
            public = True
        related_card = Card.objects.get(id=card)
        whatami = ContentType.objects.get(model="Card")
        u = User.objects.get(username=request.user)
        if comment_form:
            comment_object = Comment.objects.create(
                owner=u,
                comment=comment_form,
                public=public,
                minutes=minutes,
                overtime=overtime,
                billable=billable,
                content_type=whatami,
                object_id=int(related_card.id)
            )

        if public_close and not comment_form:
            # TODO: update tracker accordingly: as of now, no tracking update for closing from here
            column_done =Columntype.objects.get(name="Done")
            board_done_column = Column.objects.get(board=related_card.board.id, usage=column_done.id)
            # if not comment_form:
            comment_object = Comment.objects.create(
            owner=u,
            comment="Closed by operator",
            public=True,
            minutes=minutes,
            overtime=overtime,
            billable=billable,
            content_type=whatami,
            object_id=int(related_card.id)
            )
            related_card.closed = True
            related_card.column = board_done_column
            related_card.save()

        # ADD COMMENT TRACKER
        ctype = ContentType.objects.get_for_model(comment_object)
        tracker = Tracker.objects.create(
            created_time=datetime.now(),
            content_type=ctype,
            object_id=comment_object.id,
            updated_fields=str(Card.objects.get(id=card).title),
            owner=userid,
            action=str("commented on "),
        )
        tracker.save()
        # END COMMENT TRACKER

        # NOTIFICATIONS
        # TODO: add/check within user / global prefs before sending (this could
        # be moved to a function in libs once we have a working model.
        # It may be worthwhile to check which user made the mod and exclude
        # him/her from notification - this should be logged in user.

        comment_message = """
## Please do not write below this line ##

A new comment has been added to a Card you participate in:

%s

For more details view https://doit.spearhead.systems/cards/editcard/%d

https://doit.spearhead.systems
"""
        # prepare to text
        soup_comment = BeautifulSoup(comment_object.comment)
        # who to send to
        watchers_email = related_card.watchers.values_list('email', flat=True)
        all_email_addresses = list(watchers_email)
        # TODO: if  there is no owner (such as when created via portal) ..
        # wrap in a try?
        try:
            all_email_addresses.append(related_card.owner.email)
        except AttributeError:
            pass

        # we remove ourselves from this notification
        if request.user.email in all_email_addresses:
            all_email_addresses.remove(request.user.email)

        for recipient in all_email_addresses:
            if comment_object.public:
                formatted_message = comment_message % (soup_comment.get_text(), int(related_card.id))
                # TODO: you get email whether you like it or not!
                # should probably due something about this
                send_mail(
                    'Re: DoIT #doit' + str(related_card.id) + " " + related_card.title,
                    formatted_message,
                    doit_myemail,
                    [recipient],
                    fail_silently=True)
            else:
                account_type = User.objects.get(email=recipient)
                # we send only to operators and superuser
                if account_type.is_superuser or account_type.profile_user.is_operator:
                    formatted_message = comment_message % (soup_comment.get_text(), int(related_card.id))
                    # TODO: you get email whether you like it or not!
                    # should probably due something about this
                    send_mail(
                        'Re: DoIT #doit' + str(related_card.id) + " " + related_card.title,
                        formatted_message,
                        doit_myemail,
                        [recipient],
                        fail_silently=True)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return JsonResponse({'status': 'NOK'}, status=500)


@login_required
def get_comment(request):
    context = RequestContext(request)
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('card', '')
        card = Card.objects.get(id=q)

        # TODO: make sure user has permission to add this comment
        # by looking at watchers, company with is_org_admin

        ctype = ContentType.objects.get_for_model(card)
        comments = Comment.objects.filter(
            content_type__pk=ctype.id,
            object_id=card.id)
        results = []
        for co in comments:
            co_json = {}
            co_json['id'] = co.id
            co_json['comment'] = co.comment
            co_json['created_time'] = str(co.created_time)
            picture = UserProfile.objects.get(user_id=co.owner.id)
            co_json['owner'] = str(picture.picture)
            results.append(co_json)
        data = json.dumps(results)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_comment_count(request):
    context = RequestContext(request)
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('card', '')
        card = Card.objects.get(id=q)

        # TODO: make sure user has permission to add this comment
        # by looking at watchers, company with is_org_admin

        ctype = ContentType.objects.get_for_model(card)
        comments = Comment.objects.filter(
            content_type__pk=ctype.id,
            object_id=card.id)
        results = [comments.count()]
        data = json.dumps(results)
    return HttpResponse(data, content_type='application/json')


@login_required
def comment(request):
    # TODO: make sure user has permission to add this comment
    # by looking at watchers, company with is_org_admin
    if request.user.profile_user.is_customer:
        return HttpResponse("You do not have permissions to view this page.")
    context = RequestContext(request)
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('term', '')
        comments = Comment.objects.all().filter(content_type="card",
                                                object_id=q)
        results = []
        for co in comments:
            co_json = {}
            co_json['id'] = co.id
            co_json['comment'] = co.comment
            # co_json['value'] = co.id  # in the form we actually need this
            #           # value to submit but would like to show
            #           # the name in the view and not the ID!!
            results.append(co_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    # mimetype = 'application/json'
    return HttpResponse(data, content_type='application/json')
