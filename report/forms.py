from django import forms

from report.models import Reports


class ReportsForm(forms.ModelForm):
	class Meta:
		model = Reports
		fields = ('title', 'company', 'owner', 'period_from', 'period_to', 'board',)
		widgets = {
			'from_date': forms.DateInput(attrs={'class':'datepicker'}),
			'to_date': forms.DateInput(attrs={'class':'datepicker'}),
			'company': forms.TextInput(),
		}
