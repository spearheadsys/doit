from django.conf.urls import url
from contact.views import contacts, addcontact, editcontact, deletecontact

urlpatterns = [
    url(r'^$', contacts, name='contacts'),
    url(r'^addcontact/$', addcontact, name='addcontact'),
    url(r'addcontact/(?P<company>\d+)', addcontact, name='addcontact'),
    url(r'editcontact/(?P<contact>\d+)', editcontact, name='editcontact'),
    url(r'deletecontact/(?P<contact>\d+)', deletecontact, name='deletecontact'),
]
