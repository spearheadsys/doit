from django.conf.urls import url
from analytics.views import reports


# we are at /cases/ here
urlpatterns = [
    url(r'^$', reports, name='reports'),
    url(r'^organization/(?P<organization>\d+)$', reports, name='reports'),
    # url(r'^kb/create/(?P<company>\d+)', createkb, name='createkb'),
]
