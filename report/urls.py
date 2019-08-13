from django.conf.urls import url
from report.views import reports


# we are at /cases/ here
urlpatterns = [
    url(r'^$', reports, name='reports'),
]
