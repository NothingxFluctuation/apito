from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileModelForm, CouponModelForm, ContactModelForm
from django.http import HttpResponse
from django.contrib import messages
import random
import string
from .models import FileModel, CouponModel
import magic
from django.core.mail import EmailMessage, send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import braintree
import sys


# Create your views here.
def t(request):
	return render(request,'terms.html')

def pp(request):
	if settings.BRAINTREE_PRODUCTION:
		braintree_env = braintree.Environment.Production
	else:
		braintree_env = braintree.Environment.Sandbox
	braintree.Configuration.configure(
		braintree_env,
		merchant_id=settings.BRAINTREE_MERCHANT_ID,
		public_key=settings.BRAINTREE_PUBLIC_KEY,
		private_key=settings.BRAINTREE_PRIVATE_KEY,

	)
	try:
		braintree_client_token = braintree.ClientToken.generate({'customer_id': user.id })
	except:
		braintree_client_token = braintree.ClientToken.generate({})
	coupon_form = CouponModelForm()
	context = {'braintree_client_token': braintree_client_token}
	return render(request,'ck.html',context)
		

def m(request):
	if settings.BRAINTREE_PRODUCTION:
		braintree_env = braintree.Environment.Production
	else:
		braintree_env = braintree.Environment.Sandbox
	braintree.Configuration.configure(
		braintree_env,
		merchant_id=settings.BRAINTREE_MERCHANT_ID,
		public_key=settings.BRAINTREE_PUBLIC_KEY,
		private_key=settings.BRAINTREE_PRIVATE_KEY,

	)
	try:
		braintree_client_token = braintree.ClientToken.generate({'customer_id': user.id })
	except:
		braintree_client_token = braintree.ClientToken.generate({})
	coupon_form = CouponModelForm()
	context = {'braintree_client_token': braintree_client_token, 'coupon_form':coupon_form}
	return render(request, 'i.html',context)

def thisabout(request):
	return render(request,'thisabout.html')

def us(request):
	return render(request, 'us.html')

def cntct(request):
	return render(request, 'cntct.html')

def p(request):
	return render(request, 'p.html')


def cpn(request):
	return render(request,'cpn.html')


def payment(request):
    nonce_from_the_client = request.POST['paymentMethodNonce']
    customer_kwargs = {
        "first_name": "mehmud",
        "last_name": "shahkar",
        "email": "bad199614@gmail.com",
    }
    customer_create = braintree.Customer.create(customer_kwargs)
    customer_id = customer_create.customer.id
    result = braintree.Transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    print(result)
    return HttpResponse('Ok')






def main(request):
	return redirect('m')


@csrf_exempt
def index(request):
	if request.method=='POST':
		file_form = FileModelForm(request.POST, request.FILES)
		print(request.POST)
		print("Errors:  ",file_form.errors.as_data())
		if file_form.is_valid():
			#disable coupon
			cpn = request.POST.get('couponinput')
			cpni = CouponModel.objects.filter(coupon=cpn)
			print('cpni',cpni)
			if len(cpni) > 0:
				cpna = CouponModel.objects.get(coupon=cpn)
				print(cpna)


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
			return render(request,'upload_success.html',{'dwnld_link':dwnld_link})
		else:
			file_form = FileModelForm()
			messages.error(request,'There was some problem with your upload.')
			return render(request,'i.html',{'file_form':file_form})
	file_form = FileModelForm()
	return render(request, 'i.html',{'file_form':file_form})


def calculate_price(request):
	b = request.GET.get('lol')
	fileslist = b.split("xxxhumkohumhisaychuraloxxx")
	print('ff: ',fileslist)
	image_ext = ['png','jpg','jpeg']
	video_ext = ['avi','flv','wmv','mov','mp4','mkv']
	price = 0
	
	for f in fileslist:
		print('FFF:', f)
		f = f.lower()
		if f.endswith('png') or f.endswith('jpg') or f.endswith('jpeg'):
			price += 1
		elif f.endswith('avi') or f.endswith('flv') or f.endswith('wmv') or f.endswith('mov') or f.endswith('mp4') or f.endswith('mkv'):
			price += 3
		else:
			pass
	
	return HttpResponse(str(price))



def aja(request):
	h = request.GET.get('name')
	h2 = request.GET.get('name2')
	h3 = request.GET.get('username')
	rspns = "Hi, {} {} {}".format(h, h2,h3)
	print(rspns)
	return HttpResponse(rspns)

def egifts_admin(request):
	if not request.user.is_superuser:
		return HttpResponse("error: not authorized")
	
	else:
		am = request.GET.get('amount')
		am = int(am)
		qnt = request.GET.get('quantity')
		qnt = int(qnt)

		if am and qnt:
			if am > 0 and qnt > 0:
				counter = 0
				codes = ""
				while counter < qnt:
					cpn = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
					cpn_obj = CouponModel.objects.create(amount=am, coupon=cpn)
					codes = codes + cpn + "\n"
					counter +=1
				return HttpResponse(codes, content_type="text/plain")
				
		return render(request,'razi.html')
	


def check_coupon(request):
	c = request.GET.get('c')
	cpn = CouponModel.objects.filter(coupon=c, active = True)

	price = request.GET.get('papa')
	print('Price: ',price)
	if len(cpn) > 0:
		cpn = CouponModel.objects.get(coupon=c)
		amount = cpn.amount
		price = int(price)
		if price > amount:
			rspns = str(int(price-amount))
			print(rspns)
			return HttpResponse(rspns)
		new_amount = amount - price
		cpn.amount = int(new_amount)
		print("new_amount,",new_amount)
		cpn.save()
		return HttpResponse("valid")
	else:
		return HttpResponse("invalid")
	

import os
import zipfile
from io import BytesIO


def file_download(request):
	url_code = request.GET.get('i')
	file_obj = get_object_or_404(FileModel, url = url_code)
	if file_obj.file_here1:
		file1_path = file_obj.file_here.path
		file2_path = file_obj.file_here1.path
		filenames = [file1_path, file2_path]
		zip_subdir = "apitofiles"
		zip_filename = "%s.zip" % zip_subdir

		response = HttpResponse(content_type='application/zip')
		zip_file = zipfile.ZipFile(response, 'w')
		for filename in filenames:
			zip_file.write(filename)
		response['Content-Disposition'] = 'attachment; filename={}'.format(zip_filename)
		return response
	crnt_filename = file_obj.file_here.name
	file_path = file_obj.file_here.path
	file_ext = crnt_filename.split('.')[-1]
	new_filename = url_code + '.' + file_ext
	
	#content type
	mime = magic.Magic(mime=True)
	ct = mime.from_file(file_path)
	response = HttpResponse(file_obj.file_here, content_type=ct)
	response['Content-Disposition'] = 'attachment; filename=%s' % new_filename

	return response

@csrf_exempt
def create_coupon(request):
	if request.method=='POST':
		print(request.POST)
		coupon_form = CouponModelForm(request.POST)
		if coupon_form.is_valid():
			coupon_obj = coupon_form.save(commit = False)
			coupon_obj.coupon = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
			coupon_obj.save()
			sender_email = coupon_obj.sender_email
			if coupon_obj.receiver_email:
				subject = "Get your coupons"
				if coupon_obj.sender_name:
					sender = coupon_obj.sender_name
				else:
					sender = coupon_obj.sender_email
				if coupon_obj.msg_for_rcvr:
					message = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\nMessage from sender: {}".format(sender, coupon_obj.coupon,coupon_obj.msg_for_rcvr)
				else:
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
			
			return render(request,'coupon_success.html')
		else:
			coupon_form = CouponModelForm()
			return render(request,'i.html',{'coupon_form':coupon_form})

	else:
		
		coupon_form = CouponModelForm()
		return render(request,'i.html',{'coupon_form':coupon_form})

@csrf_exempt
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



