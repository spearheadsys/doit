from django import forms
from dal import autocomplete
from organization.models import Organization


class AddOrganizationsForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = (
            'name', 'description', 'owner', 'billing_address', 'billing_zip_code', 'billing_city', 'billing_country',
            'bank', 'iban', 'registration_code', 'registration_code', 'vat_number')
        widgets = {
            'description': forms.Textarea(attrs={'rows':'4', 'class': 'input-sm', 'cols':'90'})
        }
