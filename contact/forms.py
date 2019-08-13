from django import forms
from django.contrib.auth.models import User
from contact.models import UserProfile


class ContactForm(forms.ModelForm):
    """ Contact form for standard contact."""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email',)


class UserProfileForm(forms.ModelForm):
    """ UserProfile form. """
    class Meta:
        model = UserProfile
        fields = ('picture', 'company', 'is_customer',)

        widgets = {
            'company': forms.Select(attrs={
                'class': 'selectpicker',
                'data-width': 'fit',
                'data-live-search': 'true',
            }),
            'is_customer': forms.HiddenInput(),
        }
