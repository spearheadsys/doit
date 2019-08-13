from django.conf.urls import url
from organization.views import organizations, add_organization, get_company, EmailDomainAutocomplete

urlpatterns = [
    url(r'^$', organizations, name='organizations'),
    url(r'addorganization/', add_organization, name='add_organization'),
    url(r'^get_company/', get_company, name='get_company'),
    url(
        r'^emaildomain-autocomplete/$',
        EmailDomainAutocomplete.as_view(create_field='domain'),
        name='emaildomain-autocomplete',
    ),
]
