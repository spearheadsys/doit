from django import forms
from attachment.models import Attachment


class AttachmentForm(forms.ModelForm):
	class Meta:
		model = Attachment
		fields = "__all__"
	widgets = {
		'description': forms.Textarea(
			attrs={
				'placeholder': 'Attachment description',
				'class': 'form-control',
				'type': 'file',
				'rows': '4',
				'style': 'width: 86%', 
				}),
	}

	def clean_file(self):
		uploaded_file = self.cleaned_data['file']
		return uploaded_file
