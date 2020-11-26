from dal import autocomplete
from dal import forms as s2forms
from django import forms
from card.models import Card, Column, Organization
from board.models import Board
from django.forms.models import inlineformset_factory



class CardsForm(forms.ModelForm):
    class Meta:
        model = Card
        # exclude = ['modified_time']
        fields = (
            # 'title',
            # 'description',
            'column',
            'priority',
            'type',
            'start_time',
            'due_date',
            'owner',
            'watchers',
            'company',
            'estimate',
            'board',
            'tags',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "Enter card title",
                'style': 'width: 86%; border: 0px; font-size: 16pt;',
            }),
            'description': forms.Textarea(),
            'board': forms.HiddenInput(),
            'estimate': forms.NumberInput(
                attrs={
                    'required': False,
                    'style': 'width: 60px; border: 1px solid #FFBBD7; text-align: center;',
                    'min': '15',
                    'step': '15',
                    'value': '15',
            }),
            'watchers': autocomplete.Select2Multiple(
                url='watcher-autocomplete',
            ),
            'tags': autocomplete.TagSelect2(

                url='tag-autocomplete'
            ),
            'company': autocomplete.Select2(
                url='company-autocomplete',
                attrs={
                    'data-placeholder': 'Select Company'
                },
            ),
            'owner': autocomplete.Select2(
                url='owner-autocomplete'
            ),
        }
        labels = {
            'title': '',
            'description': '',
            'column': 'Choose the column',
            'tags': '',
        }

    def __init__(self, board_id=None, company=None, **kwargs):
        super(CardsForm, self).__init__(**kwargs)
        # remove the ---- / empty option from the select widget
        self.fields['column'].empty_label = None

        # I guess I was looking to make sure that the column assigned belongs to the
        # the right board...but the company?
        if board_id:
            self.fields["column"].queryset = Column.objects.filter(board=board_id)
        if company:
            self.fields["company"].queryset = Organization.objects.filter(id=company)
            # self.helper = FormHelper(self)
        # show only related watchers (i.e. contacts assigned to organization)


class EditCardForm(forms.ModelForm):
    class Meta:
        model = Card
        # exclude = ['modified_time']
        fields = (
            'title',
            'column',
            'priority',
            'type',
            'start_time',
            'due_date',
            'owner',
            'watchers',
            'company',
            'board',
            'tags',
            'estimate',
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'uk-input uk-form-width-expand'

            }),
            'board': forms.HiddenInput(),
            'start_time': forms.TextInput(
                attrs={
                    'class': 'uk-input',
                }
            ),
            'due_date': forms.TextInput(
                attrs={
                    'class': 'uk-input',
                    'style': 'width: 100%;',
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'select',
                    'style': 'width:99%',
                }),
            'priority': forms.Select(
                attrs={
                    'class': 'select',
                    'style': 'width:99%',
                }),
            'column': forms.Select(
                attrs={
                    'class': 'uk-input'
                }),
            'watchers': autocomplete.ModelSelect2Multiple(
                url='watcher-autocomplete',
                attrs={
                    'data-placeholder': 'Watchers?',
                    'class': 'uk-input uk-text-small',
                    'style': 'width: 45px;'
                }
            ),
            'company': autocomplete.ModelSelect2(
                url='company-autocomplete',
                attrs={
                    'class': 'uk-input ',
                }
            ),
            'owner': autocomplete.Select2(
                url='owner-autocomplete',
                attrs={
                    'class': 'uk-input uk-form-small',
                    'data-placeholder': 'Owner?'
                }
            ),
            'tags': autocomplete.TaggitSelect2(
                url='tag-autocomplete',
                attrs={
                    'class': 'uk-input',
                }),
            'estimate': forms.NumberInput(
                attrs={
                    'step': '15',
                    'class': 'uk-input uk-form-width-small uk-form-small',
                }),
        }



class EditColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ('title', 'board', 'wip', 'order')
        force_update = True
        # TODO: add widget to limit wiup only to positive numbers


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ("__all__")



AddColumnForm = inlineformset_factory(
    Board,
    Column,
    extra=10,
    fields="__all__")
BoardFormSet = inlineformset_factory(Board, Column, extra=4, fields="__all__")
