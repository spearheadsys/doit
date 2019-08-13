from django import forms
from board.models import Board
from dal import autocomplete


class BoardsForm(forms.ModelForm):
    field_order=['name', 'description', 'due_date']
    class Meta:
        model = Board
        exclude = ['order', 'archived', 'mailbox']
        fields = "__all__"
        widgets = {
            'name':  forms.TextInput(attrs={
                'placeholder': "Give your board a name",
                'class': "uk-input"
            }),
            'description': forms.Textarea(attrs={
                'placeholder':'What is this board going to be used for?', 
                'rows': '5',
                'class': 'uk-textarea'
            }),
            'company': autocomplete.Select2(
                url='company-autocomplete',
                attrs={
                    'data-placeholder': 'Select a Customer company',
                    'class': 'uk-input'
                },
            ),
            'owner': autocomplete.Select2(
                url='owner-autocomplete',
                attrs={
                    'data-placeholder': 'Select an owner for this Board',
                    'class': 'uk-input'
                },
            ),
            'contacts': autocomplete.Select2Multiple(
                url='contact-autocomplete',
                attrs={
                    'data-placeholder': 'Select contacts that should access this Board',
                    'class': 'uk-input'
                },
            ),
            'due_date': forms.TextInput(
                attrs={
                    'placeholder': 'Select a due date for this Board',
                    'class': 'uk-input'
                },
            ),
            'color': forms.Select(
                attrs={
                    'class': 'uk-input',

                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'uk-input',
                }
            ),
        }
        labels = {
            'name': '',
            'description': '',
            'company': '',
            'contacts': '',
            'owner': '',
            'due_date': '',
            'color': '',
            'type': '',
        }


class EditBoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = "__all__"
        widgets = {
            'description': forms.Textarea(attrs={'rows':'4', 'class': 'input-sm', 'cols':'90'}),
            'color': forms.Select(attrs={'style': 'background-color: #fff888'}),
        }
        force_update = True


