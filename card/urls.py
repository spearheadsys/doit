from django.conf.urls import url
from card.views import cards, addcard, update_card_order, addColumn, \
    editCard, editColumn, addtask, get_tasks, \
    get_task_count, update_task, movecard, deleteCard, \
    get_users, get_watchers, mailpost, calendar, add_reminder, \
    get_reminders, delete_reminder, closecard, reopencard, \
    TagAutocomplete, WatcherAutocomplete, CompanyAutocomplete, OwnerAutocomplete, \
    movecardtoboard, get_reminders_count


# we are at /cards/ here
urlpatterns = [
    url(r'^$', cards, name='cards'),
    url(r'calendar', calendar, name='calendar'),
    url(r'board/(?P<board>\d+)', cards, name='cards'),
    url(r'addcard/', addcard, name='addCard'),
    url(r'updatecardorder/', update_card_order, name='update card order'),
    url(r'addcolumn/', addColumn, name='addColumn'),
    url(r'editcard/(?P<card>\d+)', editCard, name='editCards'),
    url(r'^closecard/(?P<card>\d+)', closecard, name='closecard'),
    url(r'^reopencard/(?P<card>\d+)', reopencard, name='reopencard'),
    # editColumnModal
    url(r'editcolumn/(?P<column>\d+)', editColumn, name='editColumn'),


    url(r'addreminder/', add_reminder, name='add_reminder'),
    url(r'getreminders/', get_reminders, name='get_reminders'),
    url(r'getreminderscount/', get_reminders_count, name='get_reminders_count'),
    url(r'deletereminder/', delete_reminder, name='delete_reminder'),
    url(r'addtask/', addtask, name='add task'),
    url(r'gettasks/', get_tasks, name='get tasks'),
    url(r'gettaskcount/', get_task_count, name='get task count'),
    url(r'updatetask/', update_task, name='update tasks'),
    url(r'movecard/', movecard, name='moveCard'),
    url(r'movecardtoboard/', movecardtoboard, name='movecardtoboard'),
    url(r'deletecard/', deleteCard, name='deleteCard'),

    # get_company ajax search
    url(r'^api/get_users/', get_users, name='get_users'),
    url(r'getwatchers/', get_watchers, name='get_watchers'),
    # tags autocomplete
    url(
        r'^tag-autocomplete/$',
        TagAutocomplete.as_view(),
        name='tag-autocomplete',
    ),
    # company autocomplete
    url(
        r'^company-autocomplete/$',
        CompanyAutocomplete.as_view(),
        name='company-autocomplete',
    ),
    # watchers autocomplete
    url(
        r'^watcher-autocomplete/$',
        WatcherAutocomplete.as_view(),
        name='watcher-autocomplete',
    ),
    # owner autocomplete
    url(
        r'^owner-autocomplete/$',
        OwnerAutocomplete.as_view(),
        name='owner-autocomplete',
    ),
    # mailgun
    url(r'^mailpost/', mailpost, name='mailpost'),
]