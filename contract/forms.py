from django import forms
from django.contrib.auth.models import User
from contract.models import Contract
from organization.models import Organization

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
