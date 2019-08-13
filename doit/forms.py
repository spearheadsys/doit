from django import forms
from django.contrib.auth.models import User
from contact.models import UserProfile
# from dal import autocomplete

class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'uk-input',
                    'disabled': '',
                    'help_text': ''
                },
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'uk-input',
                    'disabled': ''
                }
            ),
        }
        labels = {
            'username': '',
            'email': '',
            'password': ''
        }

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None



class EditCustomerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("picture", "timezone", "company")
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'uk-input',
                    'disabled': ''
                }
            ),

        }

