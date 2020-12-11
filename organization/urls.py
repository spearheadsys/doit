from django.conf.urls import url
from organization.views import organizations, get_company, \
    delete_organization, all_companies_dt
    #, knowledge_base

urlpatterns = [
    url(r'^$', organizations, name='organizations'),
    url(r'^all_companies_dt', all_companies_dt, name='all_companies_dt'),
    url(r'^get_company/', get_company, name='get_company'),
    url(r'^delete_organization/(?P<company>\d+)', delete_organization, name='delete_organization'),
    #url(r'^knowledge_base/(?P<company>\d+)', knowledge_base, name='knowledge_base'),
]
