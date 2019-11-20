from django import forms
from .models import FileModel, CouponModel, ContactModel

ch = [('im','Image'),('vid','Video')]

class UploadForm(forms.Form):
	File_type = forms.ChoiceField(label="File Type", choices=ch, widget=forms.Select(choices=ch))

class FileModelForm(forms.ModelForm):
	class Meta:
		model = FileModel
		fields = ('file_type','file_here','text','file_here1','text1')

		labels = {
			"file_here" : ("Select File"),
		}

		
class CouponModelForm(forms.ModelForm):
	receiver_email = forms.EmailField(label="Receiver's Email",required=True, widget=forms.EmailInput(attrs={'maxlength':150}))
	sender_email = forms.EmailField(label="Your Email",required=True, widget=forms.EmailInput(attrs={'maxlength':150}))
	class Meta:
		model = CouponModel
		fields = ('amount','receiver_email','msg_for_rcvr','sender_name','sender_email',)

		labels = {
			"receiver_email" : ("Receiver's Email"),
			"msg_for_rcvr" : ("Message for Receiver"),
			"sender_name" : ("Your Name"),
			"sender_email" : ("Your Email"),
		}
	

class ContactModelForm(forms.ModelForm):
	class Meta:
		model = ContactModel

		fields = ('first_name','last_name','email','message')