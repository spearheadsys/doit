from django.conf.urls import url
from board.views import boards, addBoard, editBoard, archived, BoardAutocomplete, getcolumns

from board import views

# we are at /cases/ here
urlpatterns = [
    url(r'^$', boards, name='boards'),
	url(r'addboard/', addBoard, name='addBoard'),
    url(r'editboard/(?P<board>\d+)', editBoard, name='editBoard'),
    url(r'archived/', archived, name='archived'),
    url(r'getcolumns/', getcolumns, name='getcolumns'),
    # company autocomplete
    url(
        r'^board-autocomplete/$',
        BoardAutocomplete.as_view(),
        name='board-autocomplete',
    ),
]
