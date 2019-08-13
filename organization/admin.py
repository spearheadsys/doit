from django.contrib import admin

from organization.models import Organization, EmailDomain


# Register your models here.
admin.site.register(Organization)
admin.site.register(EmailDomain)

