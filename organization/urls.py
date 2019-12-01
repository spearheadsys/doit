from django.conf.urls import url
from organization.views import organizations, add_organization, get_company, \
    EmailDomainAutocomplete, delete_organization
    #, knowledge_base

urlpatterns = [
    url(r'^$', organizations, name='organizations'),
    url(r'addorganization/', add_organization, name='add_organization'),
    url(r'^get_company/', get_company, name='get_company'),
    url(r'^delete_organization/(?P<company>\d+)', delete_organization, name='delete_organization'),
    #url(r'^knowledge_base/(?P<company>\d+)', knowledge_base, name='knowledge_base'),
    url(
        r'^emaildomain-autocomplete/$',
        EmailDomainAutocomplete.as_view(create_field='domain'),
        name='emaildomain-autocomplete',
    ),
]
