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
    price = request.POST['pp']
    print(price)
    customer_kwargs = {
        "first_name": "apito",
        "last_name": "apito",
        "email": "apebbleintheocean@gmail.com",
    }
    customer_create = braintree.Customer.create(customer_kwargs)
    customer_id = customer_create.customer.id
    result = braintree.Transaction.sale({
        "amount": price,
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
	image_ext = ['png','jpg','jpeg','heic','gif']
	video_ext = ['avi','flv','wmv','mov','mp4','mkv']
	price = 0
	
	for f in fileslist:
		print('FFF:', f)
		f = f.lower()
		if f.endswith('png') or f.endswith('jpg') or f.endswith('jpeg') or f.endswith('heic') or f.endswith('gif'):
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
		if am:
			am = int(am)
		qnt = request.GET.get('quantity')
		if qnt:
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
			cpn.amount = 0
			cpn.save()
			rspns = str(int(price-amount))
			print(rspns)
			return HttpResponse(rspns)
		new_amount = amount - price
		cpn.amount = int(new_amount)
		print("new_amount,",new_amount)
		cpn.save()
		rsp = "valid " + str(new_amount)
		return HttpResponse(rsp)
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
		sender_email = request.POST['sender_email']
		sender_name = request.POST['sender_name']

		amount = request.POST['amount']
		amount1 = request.POST['amount1']
		amount2 = request.POST['amount2']
		amount3 = request.POST['amount3']
		amount4 = request.POST['amount4']

		amounts = (amount, amount1, amount2, amount3, amount4)


		receiver1email = request.POST['receiver1email']
		receiver2email = request.POST['receiver2email']
		receiver3email = request.POST['receiver3email']
		receiver4email = request.POST['receiver4email']
		receiver5email = request.POST['receiver5email']

		#receivers = {1: receiver1email, 2: receiver2email, 3: receiver3email, 4: receiver4email, 5: receiver5email}
		receivers = (receiver1email, receiver2email, receiver3email, receiver4email, receiver5email)

		receiver1message = request.POST['receiver1message']
		receiver2message = request.POST['receiver2message']
		receiver3message = request.POST['receiver3message']
		receiver4message = request.POST['receiver4message']
		receiver5message = request.POST['receiver5message']

		#messages = {1: receiver1message, 2: receiver2message, 3: receiver3message, 4: receiver4message, 5: receiver5message}
		messages = (receiver1message, receiver2message, receiver3message, receiver4message, receiver5message)

		send_codes = []

		cnt = 0
		for r in receivers:
			amount = amounts[cnt]
			if '.' in amount:
				amount = int(amount.split('.')[0])
			if r !='' and int(amount) > 0:
				coupon = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
				m = messages[cnt]
				CouponModel.objects.create(amount=amount, coupon=coupon, receiver_email=r, msg_for_rcvr = m, sender_name=sender_name, sender_email=sender_email)
				receiver = r
				if messages[cnt] != '':
					message = messages[cnt]
					subject = 'Get your coupons'
					if sender_name:
						msg = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\nMessage from sender: {}".format(sender_name, coupon, message)
					else:
						msg = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\nMessage from sender: {}".format(sender_email, coupon, message)
					print(send_mail(subject,msg, 'apebbleintheocean@gmail.com',[receiver]))
				else:
					subject = 'Get your coupons'
					if sender_name:
						msg = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\n".format(sender_name,coupon)
					else:
						msg = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\n".format(sender_email, coupon)
					print(send_mail(subject,msg,'apebbleintheocean@gmail.com',[receiver]))
				
				send_codes.append(coupon)
			cnt +=1


		sender_subject = "Generated Coupons"
		cpns = '   '.join(send_codes)
		msg = "Hi there, Please note your generated coupon codes: {}".format(cpns)
		print(send_mail(sender_subject, msg, 'apebbleintheocean@gmail.com',[sender_email]))
		return render(request,'coupon_success.html')
	return render('/')



def donation_success(request):
	return render(request, 'donation_success.html')



