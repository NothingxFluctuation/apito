from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileModelForm, CouponModelForm, ContactModelForm
from django.http import HttpResponse
from django.contrib import messages
import random
import string
from .models import FileModel, CouponModel, ExtraInfo, PaymentProgress, Funds
import magic
from django.core.mail import EmailMessage, send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import braintree
import sys
from django.core.mail import EmailMultiAlternatives
import stripe

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
	request.session['foo'] = 'bar'
	"""Need to replace these with live keys in production for apple pay to work"""
	# stripe.api_key = ""

	# stripe.ApplePayDomain.create(
 #  		domain_name='apebbleintheocean.com',
	# )


	coupon_form = CouponModelForm()
	ppf = PaymentProgress.objects.all()
	if ppf:
		PaymentProgressObject = PaymentProgress.objects.latest('id')
		PaymentProgressAmount = PaymentProgressObject.amount_paid
		fund = Funds.objects.latest('id')
		funding_required = fund.funds_required
		AllPaymentProgress = int(PaymentProgressAmount * 100 / funding_required)
		print("ApP: ",AllPaymentProgress)
		if AllPaymentProgress >= 99:
			bleach = False #Random name
			remaining_pebbles = fund.limited_pebbles
		else:
			bleach = True
			remaining_pebbles = fund.limited_pebbles



	else:
		PaymentProgressAmount = 0
		fund = Funds.objects.latest('id')
		funding_required = fund.funds_required
		AllPaymentProgress = int(PaymentProgressAmount * 100 / funding_required)
		bleach = True
		remaining_pebbles = None


	context = {'braintree_client_token': braintree_client_token, 'coupon_form':coupon_form, 'AllPaymentProgress':AllPaymentProgress,'bleach':bleach,'remaining_pebbles':remaining_pebbles}
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
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
from django.http import JsonResponse

def secret(request):
	if request.session['foo'] =='bar':
		print('ye b running')
		intent = stripe.PaymentIntent.create(
			amount=100,
			currency='usd',
			metadata={'integration_check':'accept_a_payment'},)

		return JsonResponse({'client_secret':intent.client_secret})
	print("ye wala b")
	amount = request.session['payable']
	amount = amount * 100
	intent = stripe.PaymentIntent.create(
		amount=amount,
		currency='usd',
		metadata={'integration_check': 'accept_a_payment'},
		)
	print(intent)
	return JsonResponse({'client_secret':intent.client_secret})


def set_price(request):
	r = request.GET.get('mprice')
	r = int(r)
	request.session['payable'] = r
	request.session['foo'] = 'langra'
	return HttpResponse(str(r))


def save_price(request):
	s = request.session['payable']
	pf = PaymentProgress.objects.filter(id=1)
	if pf:
		pp = PaymentProgress.objects.get(id=1)
	else:
		pp = PaymentProgress.objects.create()
	pp.amount_paid = pp.amount_paid + s 
	pp.save()
	print('ppppppp',pp.amount_paid)

	PaymentProgressAmount = pp.amount_paid
	fund = Funds.objects.latest('id')
	funding_required = fund.funds_required
	AllPaymentProgress = int(PaymentProgressAmount * 100 / funding_required)
	if AllPaymentProgress >= 99:
		pp.pebble_meter = True
		pp.save()



	return HttpResponse('ok') 




def payment(request):
    # nonce_from_the_client = request.POST['paymentMethodNonce']
    # price = request.POST['pp']
    # print(price)
    # customer_kwargs = {
    #     "first_name": "apito",
    #     "last_name": "apito",
    #     "email": "apebbleintheocean@gmail.com",
    # }
    # customer_create = braintree.Customer.create(customer_kwargs)
    # customer_id = customer_create.customer.id
    # result = braintree.Transaction.sale({
    #     "amount": price,
    #     "payment_method_nonce": nonce_from_the_client,
    #     "options": {
    #         "submit_for_settlement": True
    #     }
    # })
    # return HttpResponse('Ok')
   if request.method =='POST':
   	charge = stripe.Charge.create(amount=500, currency='usd',description='apito charge',source=request.POST.get('stripeToken'))
   	print("Stripe Token: ",request.POST.get('stripeToken'))
   	print("Charge: ",charge)
   	return HttpResponse('Ok')






def main(request):
	return redirect('home')


@csrf_exempt
def index(request):
	if request.method=='POST':
		try:
			file_form = FileModelForm(request.POST, request.FILES)
			print(request.POST)
			print("Errors:  ",file_form.errors.as_data())

			#disable coupon
			cpn = request.POST.get('couponinput')
			cpni = CouponModel.objects.filter(coupon=cpn)
			print('cpni',cpni)
			if len(cpni) > 0:
				cpna = CouponModel.objects.get(coupon=cpn)
				print(cpna)



			new_file = file_form.save()
			order_no = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
			new_file.order_no = order_no
			new_file.save()

			pf = PaymentProgress.objects.filter(id=1)
			if pf:
				pp = PaymentProgress.objects.get(id=1)
				if pp.pebble_meter:
					cnt = 0
					if new_file.file_here:
						cnt += 1
					if new_file.file_here1:
						cnt +=1
					if new_file.file_here2:
						cnt +=1
					if new_file.file_here3:
						cnt +=1
					if new_file.file_here4:
						cnt +=1
					

					f= Funds.objects.latest('id')
					lp = f.limited_pebbles
					new_lp = lp - cnt 
					f.limited_pebbles = new_lp
					f.save()
				else:
					pass
			else:
				pass
			rsp = order_no
			em = request.POST.get('emailforid',None)
			print(em)
			if em:
				subject = "Your Apito Order Number"
				text_content = "Apito Order Number Notification"
				from_email = 'apebbleintheocean@gmail.com'
				to = em
				html_content = '<p>Hello there,</p><p>Here is the order number for the pebbles you uploaded through Apito:</p><p>{}</p><p>Keep this order number to be able to reference the pebbles you uploaded. You will also need this order number later on to find your pebbles when the time capsule is reopened.</p><p>On behalf of Apito, thank you for your contribution.<p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format(order_no)
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
				msg.attach_alternative(html_content,"text/html")
				msg.send()
				print(msg)


			return HttpResponse(rsp)
		except:
			return HttpResponse('something bad happened')
# #		else:
#			file_form = FileModelForm()
#			messages.error(request,'There was some problem with your upload.')
#			return render(request,'i.html',{'file_form':file_form})
	file_form = FileModelForm()
	return redirect('/')


@csrf_exempt
def getextra(request):
	if request.method=='POST':
		idofform = request.POST.get('idoffileform')
		if idofform:
			intid = int(idofform)
			form = FileModel.objects.get(id=intid)
		else:
			return render(request, 'upload_success.html')
		rinfo = request.POST.get('info')
		if rinfo:
			exinfo = rinfo
		else:
			exinfo = ''
		country = request.POST.get('country')
		if country:
			excountry = country
		else:
			excountry = ''
		ExtraInfo.objects.create(file=form, info=exinfo, country=excountry)
		return render(request,'upload_success.html')





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
		if cpn.amount == 0:
			cpn.delete()
		rsp = "valid " + str(new_amount)
		return HttpResponse(rsp)
	else:
		return HttpResponse("invalid")



import csv
from django.utils.encoding import smart_str

def download_csv(request):
	if not request.user.is_superuser:
		return HttpResponse('denied.')
	fmobjects = FileModel.objects.all()
	response = HttpResponse(content_type='text/css')
	response['Content-Disposition'] = 'attachment; filename=apitodata.csv'
	writer = csv.writer(response,csv.excel)
	response.write(u'\ufeff'.encode('utf8'))
	writer.writerow([
		smart_str(u"ID"),
		smart_str(u"File0 Type"),
		smart_str(u"File0"),
		smart_str(u"Text0"),
		smart_str(u"File1 Type"),
		smart_str(u"File1"),
		smart_str(u"Text1"),
		smart_str(u"File2 Type"),
		smart_str(u"File2"),
		smart_str(u"Text2"),
		smart_str(u"File3 Type"),
		smart_str(u"File3"),
		smart_str(u"Text3"),
		smart_str(u"File4 Type"),
		smart_str(u"File4"),
		smart_str(u"Text4"),
		smart_str(u"Duration"),
		smart_str(u"Country"),
		smart_str(u"Uploaded At"),

	])

	for object in fmobjects:
		writer.writerow([
			smart_str(object.id),
			smart_str(object.file_type),
			smart_str(object.file_here),
			smart_str(object.text),
			smart_str(object.file_type1),
			smart_str(object.file_here1),
			smart_str(object.text1),
			smart_str(object.file_type2),
			smart_str(object.file_here2),
			smart_str(object.text2),
			smart_str(object.file_type3),
			smart_str(object.file_here3),
			smart_str(object.text3),
			smart_str(object.file_type4),
			smart_str(object.file_here4),
			smart_str(object.text4),
			smart_str(object.info),
			smart_str(object.country),
			smart_str(object.created),
			])
	return response





import shutil
from django.conf import settings
from wsgiref.util import FileWrapper
import os
from django.http import FileResponse



def download_all_files(request):
	if request.user.is_superuser:

		path = settings.MEDIA_ROOT + 'file_content'
		archive_name = settings.MEDIA_ROOT + 'apito-media-files'
		shutil.make_archive(archive_name,'zip',path)
		filename = archive_name + '.zip'
		print('ff: ',filename)
		# wrapper = FileWrapper(file(filename))
		# response = HttpResponse(wrapper, content_type='text/plain')
		# response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
		# response['Content-Length'] = os.path.getsize(filename)
		# myfile = open(filename,'rb').read()
		# response = FileResponse(myfile, content_type="application/zip")
		# response['Content-Disposition'] = 'attachment; filename=apito-media-files.zip'
		fl = open('E://DP/apito/apito/media/apito-media-files.zip','rb')
		response = FileResponse(fl)
		return response
	return HttpResponse("denied.")






import zipfile
from io import BytesIO
import os

def file_download_url(request):
	mr = settings.MEDIA_ROOT + 'apito_files'
	if not os.path.exists(mr):
		os.mkdir(mr)

	files = FileModel.objects.all()

	for file in files:
		if file.order_no:
			order_no = file.order_no
			order_dir = mr + '/' + str(order_no)
			if not os.path.exists(order_dir):
				os.mkdir(order_dir)
			file_here = file.file_here
			file_here1 = file.file_here1
			file_here2 = file.file_here2
			file_here3 = file.file_here3
			file_here4 = file.file_here4
			if file_here:
				file_here_path = file_here.path 
				pebble_dir = order_dir + '/pebble_1'
				if not os.path.exists(pebble_dir):
					os.mkdir(pebble_dir)
				p = file_here.path.split('.')[1]
				new = pebble_dir + '/pebble_1.' + p
				shutil.copyfile(file_here.path, new)
				if file.text:
					print("yes text is here")
					txt = file.text
					print(txt)
					txt_file = pebble_dir + '/pebble_1.txt'
					print(txt_file)
					infile = open(txt_file,'w')
					infile.write(txt)
					infile.close()
			if file_here1:
				file_here1_path = file_here1.path 
				pebble_dir1 = order_dir + '/pebble_2'
				if not os.path.exists(pebble_dir1):
					os.mkdir(pebble_dir1)
				p = file_here1.path.split('.')[1]
				new = pebble_dir1 + '/pebble_2.' + p
				shutil.copyfile(file_here1.path, new)
				if file.text1:
					txt = file.text1
					txt_file = pebble_dir1 + '/pebble_2.txt'
					infile = open(txt_file,'w')
					infile.write(txt)
					infile.close()
			if file_here2:
				file_here2_path = file_here2.path 
				pebble_dir2 = order_dir + '/pebble_3'
				if not os.path.exists(pebble_dir2):
					os.mkdir(pebble_dir2)
				p = file_here2.path.split('.')[1]
				new = pebble_dir2 + '/pebble_3.' + p
				shutil.copyfile(file_here2.path, new)
				if file.text2:
					txt = file.text2
					txt_file = pebble_dir2 + '/pebble_3.txt'
					infile = open(txt_file,'w')
					infile.write(txt)
					infile.close()

			if file_here3:
				file_here3_path = file_here3.path 
				pebble_dir3 = order_dir + '/pebble_4'
				if not os.path.exists(pebble_dir3):
					os.mkdir(pebble_dir3)
				p = file_here3.path.split('.')[1]
				new = pebble_dir3 + '/pebble_4.' + p
				shutil.copyfile(file_here3.path, new)
				if file.text3:
					txt = file.text3
					txt_file = pebble_dir3 + '/pebble_4.txt'
					infile = open(txt_file,'w')
					infile.write(txt)
					infile.close()
			if file_here4:
				file_here4_path = file_here4.path 
				pebble_dir4 = order_dir + '/pebble_5'
				if not os.path.exists(pebble_dir4):
					os.mkdir(pebble_dir4)
				p = file_here4.path.split('.')[1]
				new = pebble_dir4 + '/pebble_5.' + p
				shutil.copyfile(file_here4.path, new)
				if file.text4:
					txt = file.text4
					txt_file = pebble_dir4 + '/pebble_5.txt'
					infile = open(txt_file,'w')
					infile.write(txt)
					infile.close()



	shutil.make_archive(mr,'zip',mr)
	return redirect('/media/apito_files.zip')
	#return HttpResponse("OK")







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
		print("Amounts: ",amounts)

		receiver1email = request.POST['receiver1email']
		receiver2email = request.POST['receiver2email']
		receiver3email = request.POST['receiver3email']
		receiver4email = request.POST['receiver4email']
		receiver5email = request.POST['receiver5email']

		#receivers = {1: receiver1email, 2: receiver2email, 3: receiver3email, 4: receiver4email, 5: receiver5email}
		receivers = (receiver1email, receiver2email, receiver3email, receiver4email, receiver5email)
		print("Rcvrz: ",receivers)

		receiver1message = request.POST['receiver1message']
		receiver2message = request.POST['receiver2message']
		receiver3message = request.POST['receiver3message']
		receiver4message = request.POST['receiver4message']
		receiver5message = request.POST['receiver5message']

		#messages = {1: receiver1message, 2: receiver2message, 3: receiver3message, 4: receiver4message, 5: receiver5message}
		messages = (receiver1message, receiver2message, receiver3message, receiver4message, receiver5message)
		print("msgz: ",messages)
		send_codes = []
		send_emails = []
		send_amounts = []
		rcv_emails = {}
		rcv_amounts = {}
		cnt = 0
		cpna = ''
		for r in receivers:
			amount = amounts[cnt]
			if '.' in amount:
				amount = int(amount.split('.')[0])
			if int(amount) > 0:
				coupon = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
				CouponModel.objects.create(amount=amount, coupon=coupon)

				if r !='':
					m = messages[cnt]
					receiver = r
					if messages[cnt] != '':
						message = messages[cnt]
						if sender_name:
							subject = '{} has sent you an Apito eGift'.format(sender_name)
							html_content = html_content = '<p>Hello there,</p><p>{} has sent you an apito eGift.</p><p>Code: {}</p><p>Amount: ${}</p><p>{}\'s message: {}</p><p>You can use the eGift to upload your pebbles through the Apito website, linked below:</p><p><a href="https://www.apebbleintheocean.com">www.apebbleintheocean.com</a></p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format(sender_name, coupon,amount, sender_name, message)
	#						msg = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\nMessage from sender: {}".format(sender_name, coupon, message)
						elif sender_email:
							subject = '{} has sent you an Apito eGift'.format(sender_email)
							html_content = html_content = '<p>Hello there,</p><p>{} has sent you an apito eGift.</p><p>Code: {}</p><p>Amount: ${}</p><p>{}\'s message: {}</p><p>You can use the eGift to upload your pebbles through the Apito website, linked below:</p><p><a href="https://www.apebbleintheocean.com">www.apebbleintheocean.com</a></p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format(sender_email, coupon,amount, sender_email, message)
						else:
							subject = '{} has sent you an Apito eGift'.format('Someone')
							html_content = html_content = '<p>Hello there,</p><p>{} has sent you an apito eGift.</p><p>Code: {}</p><p>Amount: ${}</p><p>{}\'s message: {}</p><p>You can use the eGift to upload your pebbles through the Apito website, linked below:</p><p><a href="https://www.apebbleintheocean.com">www.apebbleintheocean.com</a></p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format('Someone', coupon,amount, 'Someone', message)

	#						msg = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\nMessage from sender: {}".format(sender_email, coupon, message)
						
	#					print(send_mail(subject,msg, 'apebbleintheocean@gmail.com',[receiver]))
						from_email = 'apebbleintheocean@gmail.com'
						to = receiver 
						text_content = 'Apito eGift Notification'
						msg = EmailMultiAlternatives(subject, text_content, from_email,[to])
						msg.attach_alternative(html_content, "text/html")
						msg.send()
					else:
						
						if sender_name:
							subject = '{} has sent you an Apito eGift'.format(sender_name)
							html_content = html_content = '<p>Hello there,</p><p>{} has sent you an apito eGift.</p><p>Code: {}</p><p>Amount: ${}</p><p>You can use the eGift to upload your pebbles through the Apito website, linked below:</p><p><a href="https://www.apebbleintheocean.com">www.apebbleintheocean.com</a></p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format(sender_name, coupon, amount, sender_name)

							#msg = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\n".format(sender_name,coupon)
						elif sender_email:
							subject = '{} has sent you an Apito eGift'.format(sender_email)
							html_content = '<p>Hello there,</p><p>{} has sent you an apito eGift.</p><p>Code: {}</p><p>Amount: ${}</p><p>You can use the eGift to upload your pebbles through the Apito website, linked below:</p><p><a href="https://www.apebbleintheocean.com">www.apebbleintheocean.com</a></p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format(sender_email, coupon, amount, sender_email)
						else:
							subject = '{} has sent you an Apito eGift'.format('Someone')
							html_content = '<p>Hello there,</p><p>{} has sent you an apito eGift.</p><p>Code: {}</p><p>Amount: ${}</p><p>You can use the eGift to upload your pebbles through the Apito website, linked below:</p><p><a href="https://www.apebbleintheocean.com">www.apebbleintheocean.com</a></p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format('Someone', coupon, amount, 'Someone')

	#						msg = "Hi there, \n\n{} sent you a coupon. Coupon Code: {}\n\n".format(sender_email, coupon)
	#					print(send_mail(subject,msg,'apebbleintheocean@gmail.com',[receiver]))
						from_email = 'apebbleintheocean@gmail.com'
						to = receiver
						text_content = 'Apito eGift Notification'
						msg = EmailMultiAlternatives(subject,text_content, from_email,[to])
						msg.attach_alternative(html_content, "text/html")
						msg.send()
					send_codes.append(coupon)
					rcv_emails[coupon] = receiver 
					rcv_amounts[coupon] = amount 
					send_emails.append(to)
					send_amounts.append(amount)
				else:
					mkmk = "<p>{} ${}</p>".format(coupon,amount)
					cpna = cpna + mkmk
			cnt +=1




		subject = "Your Apito eGifts"
		#cpns = '   '.join(send_codes)
		cpn = ''
		for idx, val in enumerate(send_codes):
			print("IDX: ",idx," Val: ",val)
			mokamail = send_emails[idx]
			print("mokamail: ",mokamail)
			mokaamount = send_amounts[idx]
			print("mokaamount: ", mokaamount)
			mokamoka ='<p>{} : {} ${}</p>'.format(mokamail, val, mokaamount)
			print("mokamoka: ",mokamoka)
			cpn = cpn + mokamoka
		coup = cpn + cpna
		if sender_email:

			if sender_name:
				pass
			else:
				sender_name = sender_email
			html_content = '<p>Hello {},</p><p>Here are the Apito eGifts you purchased:</p>'.format(sender_name) + cpn + '<p>On behalf of Apito, thank you for your contribution.</p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'
			from_email = 'apebbleintheocean@gmail.com'
			to = sender_email
			text_content = 'Apito eGift Notification'
			msg = EmailMultiAlternatives(subject,text_content, from_email,[to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			#msg = "Hi there, Please note your generated coupon codes: {}".format(cpns)
	#		print(send_mail(sender_subject, msg, 'apebbleintheocean@gmail.com',[sender_email]))
		return HttpResponse(coup)
	return render(request,'coupon_success.html')
	#return redirect('/')



def donation_success(request):
	m = request.META['HTTP_USER_AGENT']
	print(m)
	return render(request, 'donation_success.html')


def oh_my_apple(request):
	return redirect('/media/apple-developer-merchantid-domain-association')