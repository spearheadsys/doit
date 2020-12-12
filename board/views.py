from django.http import HttpResponseRedirect, HttpResponse
from django.urls import resolve
from django.template import RequestContext
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
import json, os
import board
from card.models import Column, Board, Card, Columntype, Comment, Attachment
from contact.models import UserProfile
from board.forms import BoardsForm, EditBoardForm
from card.forms import ColumnForm, AddColumnForm
from django.conf import settings
from datetime import date, datetime
from django.db.models import Q, Max
from django.contrib.contenttypes.models import ContentType
from doit.models import Tracker
from collections import OrderedDict
from django.views.decorators.csrf import csrf_exempt
from dal import autocomplete
from taggit.models import Tag
# GLOBALS
doitVersion = settings.DOIT_VERSION

# TODO: how do we make sure that a user/customer is not accesing a board which
# he is not a contact / watcher for?

@login_required
def boards(request):
    today_date = date.today()
    current_url = resolve(request.path_info).url_name
    u = User.objects.get(username=request.user)
    up = u.profile_user
    if up.is_customer:
        return HttpResponse("You do not have permissions to view this page.")
    boards = Board.objects.all().select_related().filter(
        archived=False).order_by('name')
    addBoardForm = BoardsForm(initial={'color': '0'})
    # context = RequestContext(request)
    addColumnForm = ColumnForm()
    list_of_stats = []

    for board in boards:
        # get the column order and identify done column
        # we assume this to be the right most column...

        try:
            board_done_order = Column.objects.filter(
            board=board).aggregate(Max('order'))['order__max']
        except:
            pass

        # print("board_done_order >>>> ", board_done_order)

        try:
            board_done_column = Column.objects.get(
                board=board,
                order=board_done_order)
        except:
            pass


        # now we get globals (not assigned just to u.id)
        all_open_cards = Card.objects.all().filter(
            closed=False,
            board=board,
        )
        all_closed_cards = Card.objects.all().filter(
            board=board,
            closed=True
        )
        all_overdue_cards = Card.objects.filter(
            ~Q(column_id=board_done_column),
            Q(due_date__lt=today_date),
            board=board,
        )
        progress = board.progress()

        # add our stats to the list
        boarddict = {
            'name': board.name,
            'progress': progress,
            'id': board.id,
            'color': board.get_color_display(),
            'board_id': board.id,
            'description': board.description,
            'allopen': all_open_cards.count(),
            'all_closed_cards': all_closed_cards.count(),
            'alloverdue': all_overdue_cards.count(),
            'board_due_date': board.due_date,
            'board_created_time': board.created_time,
        }
        list_of_stats.append(boarddict)


    # totals
    all_open_cards = 0
    all_overdue_cards = 0
    for item in list_of_stats:
        all_open_cards += item['allopen']
        all_overdue_cards += item['alloverdue']

    context_dict = {
        'site_title': "Boards | Spearhead Systems",
        'page_name': "Boards",
        'active_url': current_url,
        'user': u,
        'userprofile': up,
        'boards': list_of_stats,
        'addBoardForm': addBoardForm,
        'addColumnForm': addColumnForm,
        'doitVersion': doitVersion,
    }
    return render(request, 'board/boards.html', context_dict)


@login_required
@csrf_exempt
def addBoard(request):
    context = RequestContext(request)
    if request.is_ajax() or request.method == 'POST':
        board_form = BoardsForm(request.POST or None, request.FILES or None)
        addColumnForm = ColumnForm(request.POST or None)
        data = request.POST.copy()
        # print("contacts are >>>>", data.getlist('contacts'))
        userid = request.user
        if board_form.is_valid():
            print("form is apparently valid >>>>>")
            new_board = board_form.save()
            board = Board.objects.get(id=new_board.pk)
            coltitles = request.POST.getlist('title')
            colusages = request.POST.getlist('usage')
            coldict = OrderedDict(zip(coltitles, colusages))
            corder = 1
            #todo: fix m2m for contacts
            for k, v in coldict.items():
                if k:
                    new_col = Column(
                        order=corder,
                        board=board,
                        title=k,
                        usage=Columntype.objects.get(id=v))
                    new_col.save()
                    corder += 1

            # ADD BOARD TRACKER
            board = Board.objects.get(id=new_board.pk)
            if board.company_id or board.owner_id is None:
                company = None
                owner = None
            else:
                company = int(board.company_id)
                owner = int(board.owner_id)
            ctype = ContentType.objects.get_for_model(board)
            # updates = {
            #     'name': board.name,
            #     'description': board.description,
            #     'company': company,
            #     'contacts': board.contacts.all(),
            #     'columns': board.column_set,
            #     'archived': board.archived,
            #     'due_date': board.due_date,
            #     'owner': owner,
            # }

            tracker = Tracker.objects.create(
                created_time=datetime.now(),
                content_type=ctype,
                object_id=board.id,
                updated_fields=str(board.name),
                owner=userid,
                action=str("added a new board named "),
            )
            tracker.save()
            # END ADD BOARD TRACKER

            # return HttpResponseRedirect('/boards/')
            return redirect('boards')
        else:
            print("This form is not valid >>>>> ", board_form.errors)
            context_dict = {
            'site_title': "Boards | Spearhead Systems",
            'page_name': "Add Board",
            'addBoardForm': board_form,
            'addColumnForm': addColumnForm,
            'doitVersion': doitVersion,
        }
            return render(request,'boards/addboard.html', context_dict)
    else:
        addBoardForm = BoardsForm(initial={'color': '0'})
        addColumnForm = ColumnForm()
        context_dict = {
            'site_title': "Boards | Spearhead Systems",
            'page_name': "Add Board",
            'addBoardForm': addBoardForm,
            'addColumnForm': addColumnForm,
            'doitVersion': doitVersion,

        }
        return render(request,'boards/addboard.html', context_dict)

@login_required
def editBoard(request, board=None):
    """
    Edit the properties of a board.
    """
    current_url = resolve(request.path_info).url_name
    instance = Board.objects.get(id=board)
    if request.method == 'POST':
        board = str(instance.id)
        # Todo: if board is previously arhived, we should reopen all cards!
        form = EditBoardForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # or should we redirect to the edited board?
            redirect_url = "/boards/"
            if instance.archived:

                # allcolumnsofthisboard = Column.objects.all().filter(board=board)
                columnDone = Columntype.objects.get(name="Done")
                # columndoneofthisboard = Column.objects.all().filter(board=board).filter(usage=columnDone)
                allcardsofthisboard = Card.objects.all().filter(board=board).filter(closed=False)

                for card in allcardsofthisboard:
                    # print(card, card.column)
                    # Do not move to Done column - it will be hard to reopen on unarchiving the board
                    # card.column = columndoneofthisboard
                    card.closed = True
                    card.save()

                # TODO: get all cards and close them
                # optionally add a closed by arhiching comment!
                # additionally reopen them once the board is re-opened
            return HttpResponseRedirect(redirect_url)
        else:
            print(form.errors)
        # this should never hit
        return HttpResponseRedirect("/home/")
    else:
        # if we are here it means we did not save anything
        # so we display it here
        context = RequestContext(request)
        board = Board.objects.get(id=board)
        form = EditBoardForm(instance=board)
        board_columns = Column.objects.filter(board=board).order_by('order')
        boards = Board.objects.filter(archived=False)
        context_dict = {
            'site_title': "Edit Board - " + str(board.name) + " | Spearhead Systems",
            'page_name': "Edit Board",
            'active_url': current_url,
            'board': board,
            'form': form,
            'board_columns': board_columns,
            'boards': boards
        }
        # return render_to_response('boards/editboard.html', context_dict, context)
        return render(request, 'boards/editboard.html', context_dict)


@login_required
def deleteBoard(request, board=None):
    """
    Delete a board.
    """
    if request.user.profile_user.is_superuser or request.user.profile_user.is_operator:
        # print("deleteBoard >>>>> ", board)
        # delete associated cards
        board_obj = Board.objects.get(id=board)
        for card in Card.objects.filter(board=board):
            # delete all comments
            for c in Comment.objects.filter(object_id=card.id):
                c.delete()
            # delete all attachments
            for a in Attachment.objects.filter(card=card.id):
                a.delete()
            # finally delete the card
            card.delete()
            # now we can remove the board
        Board.objects.get(id=board).delete()
        try:
            # remove board from filesystem
            os.rmdir('media/uploads/{}'.format(board_obj.id))
        except OSError as e:
            print("Error: board_id: %s : %s" % (board_obj.id, e.strerror))
    return HttpResponseRedirect('/boards')


# archived boards are here
# TODO: make these read-only
@login_required
def archived(request):
    current_url = resolve(request.path_info).url_name
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
    ##
    # trying to get user and group in same filed
    users = User.objects.all()
    groups = Group.objects.all()
    ug = list(users) + list(groups)
    #

    # TODO: if board is empty (i.e. no columns) we should trigger something
    # like a wizard or autocreate

    boards = Board.objects.all().filter(archived=True)
    addBoardForm = BoardsForm()
    context = RequestContext(request)
    addColumnForm = AddColumnForm()

    context_dict = {
        'site_title': "Boards | Spearhead Systems",
        'page_name': "Archived boards",
        'active_url': current_url,
        'user': u,
        'userprofile': up,
        'boards': boards,
        'addBoardForm': addBoardForm,
        'addColumnForm': addColumnForm,
    }
    # return render_to_response('boards/archived.html', context_dict, context)
    return render(request, 'boards/archived.html', context_dict)


@login_required
def getcolumns(request):
    if request.is_ajax() or request.method == 'POST':
        boardid = request.POST['arr']
        boardcolumns = Column.objects.all().filter(board=boardid)
        results = []
        for col in boardcolumns:
            col_json = {}
            col_json['id'] = col.id
            col_json['title'] = col.title
            results.append(col_json)
        data = json.dumps(results)
    return HttpResponse(data, content_type='application/json')


# watchers for autocomplete
class BoardAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Board.objects.all().filter(archived=False)

        if self.q:
             qs = qs.filter(name__icontains=self.q)

        return qs

