from django import forms
from comment.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'comment',
            'public',
            'billable',
            'overtime',
            'minutes'
        )
        widgets = {
            'comment': forms.Textarea(
            ),
            'minutes': forms.NumberInput(
                attrs={
                    'class': 'uk-input uk-form-danger',
                    'required': True,
                    'style': 'width: 60px; border: 1px solid #FFBBD7; text-align: center;',
                    'min': '0',
                    'step': '15',
                    'value': 0,
                }),
        }
        labels = {
            'public': 'Public?',
        }
