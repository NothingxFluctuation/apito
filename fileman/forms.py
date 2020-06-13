from django import forms
from .models import FileModel, CouponModel

ch = [('im','Image'),('vid','Video')]

class UploadForm(forms.Form):
	File_type = forms.ChoiceField(label="File Type", choices=ch, widget=forms.Select(choices=ch))

class FileModelForm(forms.ModelForm):
	class Meta:
		model = FileModel
		exclude = ('created',)

		labels = {
			"file_here" : ("Select File"),
		}

		
class CouponModelForm(forms.ModelForm):
	class Meta:
		model = CouponModel
		fields = ('__all__')

	