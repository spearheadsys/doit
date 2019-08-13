from django.contrib import admin
from contract.models import Contract, Sla

# Register your models here.
admin.site.register(Contract)
admin.site.register(Sla)

class ContractAdmin(admin.ModelAdmin):
    """ """
    model = Contract
    list_display = ('name', 'active')
    verbose_name = "Contract"


class SlaAdmin(admin.ModelAdmin):
    """ """
    model = Sla
    list_display = ('name', 'response_time')
    verbose_name = "SLA"
