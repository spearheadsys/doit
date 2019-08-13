from django.conf.urls import url
from contract.views import contracts, addcontract, editcontract, deletecontract

urlpatterns = [
    url(r'^$', contracts, name='contracts'),
    url(r'^addcontract/$', addcontract, name='addcontract'),
    url(r'addcontract/(?P<company>\d+)', addcontract, name='addcontract'),
    url(r'editcontract/(?P<contract>\d+)', editcontract, name='editcontract'),
    url(r'deletecontract/(?P<contract>\d+)', deletecontract, name='deletecontract'),
]
