from django.conf.urls import url
from card.views import cards, addcard, update_card_order, addColumn, \
    editCard, editColumn, movecard, deleteCard, \
    get_users, get_watchers, mailpost, calendar, closecard, reopencard, \
    TagAutocomplete, WatcherAutocomplete, CompanyAutocomplete, OwnerAutocomplete, \
    movecardtoboard, getCardSlaStatus

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
    url(r'movecard/', movecard, name='moveCard'),
    url(r'movecardtoboard/', movecardtoboard, name='movecardtoboard'),
    url(r'deletecard/(?P<card>\d+)', deleteCard, name='deleteCard'),

    url(r'^cardsla/(?P<card>\d+)', getCardSlaStatus, name='getCardSlaStatus'),

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