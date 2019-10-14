from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileModelForm, CouponModelForm, ContactModelForm
from django.http import HttpResponse
from django.contrib import messages
import random
import string
from .models import FileModel, CouponModel
import magic
from django.core.mail import EmailMessage, send_mail
# Create your views here.


def main(request):
	return redirect('product')

def index(request):
	if request.method=='POST':
		file_form = FileModelForm(request.POST, request.FILES)
		print(request.POST)
		print("Errors:  ",file_form.errors.as_data())
		if file_form.is_valid():
			#disable coupon
			cpn = request.POST.get('couponinput')
			cpni = CouponModel.objects.filter(coupon=cpn, active = True)
			if len(cpni) > 0:
				cpna = CouponModel.objects.get(coupon=cpn, active=True)
				cpna.active = False
				cpna.save()


			new_file = file_form.save(commit=False)
			url_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(40))
			new_file.url = url_code
			chki = request.POST.get('chki')
			if chki:
				if chki == 'on':
					new_file.info = 'student'
			country = request.POST.get('country')
			if country:
				new_file.country = country
			new_file.save()
			dwnld_link = "http://127.0.0.1:8000/dwnid/?i=" + new_file.url
			rspns = "File successfully uploaded. share this download link {}".format(dwnld_link)
			return HttpResponse(rspns)
		else:
			file_form = FileModelForm()
			messages.error(request,'There was some problem with your upload.')
			return render(request,'index.html',{'file_form':file_form})
	file_form = FileModelForm()
	return render(request, 'index.html',{'file_form':file_form})


def aja(request):
	h = request.GET.get('name')
	h2 = request.GET.get('name2')
	h3 = request.GET.get('username')
	rspns = "Hi, {} {} {}".format(h, h2,h3)
	print(rspns)
	return HttpResponse(rspns)


def check_coupon(request):
	c = request.GET.get('c')
	cpn = CouponModel.objects.filter(coupon=c, active = True)
	if len(cpn) > 0:
		return HttpResponse("valid")
	else:
		return HttpResponse("invalid")
	




def file_download(request):
	url_code = request.GET.get('i')
	file_obj = get_object_or_404(FileModel, url = url_code)
	file_path = file_obj.file_here.path 
	crnt_filename = file_obj.file_here.name
	file_ext = crnt_filename.split('.')[-1]
	new_filename = url_code + '.' + file_ext
	
	#content type
	mime = magic.Magic(mime=True)
	ct = mime.from_file(file_path)
	response = HttpResponse(file_obj.file_here, content_type=ct)
	response['Content-Disposition'] = 'attachment; filename=%s' % new_filename

	return response

def create_coupon(request):
	if request.method=='POST':
		coupon_form = CouponModelForm(request.POST)
		if coupon_form.is_valid():
			coupon_obj = coupon_form.save(commit = False)
			coupon_obj.coupon = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
			coupon_obj.save()
			if coupon_obj.receiver_email:
				subject = "Get your coupons"
				if coupon_obj.sender_name:
					sender = coupon_obj.sender_name
				else:
					sender = coupon_obj.sender_email
				message = "Hi there,\n\n{} sent you a coupon. Coupon Code: {}".format(sender, coupon_obj.coupon)
				print(send_mail(subject, message, 'admin@project.com',[coupon_obj.receiver_email]))
			if coupon_obj.sender_email:
				subject = "Generated coupons"
				if coupon_obj.sender_name:
					sender = coupon_obj.sender_name
				else:
					sender = coupon_obj.sender_email
				message = "Hi there,\n\n{} you have generated this coupon code: {}".format(sender, coupon_obj.coupon)
				print(send_mail(subject,message,'admin@project.com',[coupon_obj.sender_email]))

			rspns = "Generated Coupon: {}".format(coupon_obj.coupon)
			return HttpResponse(rspns)
		else:
			coupon_form = CouponModelForm()
			return render(request,'coupon.html',{'coupon_form':coupon_form})

	else:
		
		coupon_form = CouponModelForm()
		return render(request,'coupon.html',{'coupon_form':coupon_form})


def contact(request):
	if request.method == 'POST':
		contact_form = ContactModelForm(request.POST)
		if contact_form.is_valid():
			contact_form.save()
			return HttpResponse("thanks for your feedback.")
		else:
			contact_form = ContactModelForm()
			return render(request,'contact.html',{'contact_form':contact_form})
	contact_form = ContactModelForm()
	return render(request,'contact.html',{'contact_form':contact_form})



