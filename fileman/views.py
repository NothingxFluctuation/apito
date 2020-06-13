#!/usr/bin/python
# -*- coding: utf-8 -*-


#import all necessary modules
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileModelForm, CouponModelForm
from django.http import HttpResponse
from django.contrib import messages
import random
import string
from .models import FileModel, CouponModel, ExtraInfo, PaymentProgress, Funds
import magic
from django.core.mail import EmailMessage, send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import re
import sys
from django.core.mail import EmailMultiAlternatives
import stripe
from django.http import JsonResponse
from django.conf import settings


#set stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.



#serve terms and conditions page
def terms(request):
    return render(request,'terms.html')


#serve main home page with all the required information
def main(request):
    request.session['foo'] = 'bar'
    request.session['pebble_form_count'] = 1
    request.session['egift_form_count'] = 1
    """Need to replace these with live keys in production for apple pay to work"""
    # stripe.api_key = ""

    # stripe.ApplePayDomain.create(
    #     domain_name='apebbleintheocean.com',
    # )


    coupon_form = CouponModelForm()
    pp_objects = PaymentProgress.objects.all()
    if pp_objects:
        PaymentProgressObject = PaymentProgress.objects.latest('id')
        PaymentProgressAmount = PaymentProgressObject.amount_paid
        fund = Funds.objects.latest('id')
        funding_required = fund.funds_required
        AllPaymentProgress = int(PaymentProgressAmount * 100 / funding_required)
        print("APP: ",AllPaymentProgress)
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

    context = {'coupon_form':coupon_form, 'AllPaymentProgress':AllPaymentProgress,'bleach':bleach,'remaining_pebbles':remaining_pebbles}
    return render(request, 'i.html',context)




#serve faq page
def faq(request):
    return render(request,'thisabout.html')


#create stripe client secret and send it to client side to receive money
def secret(request):
    if request.session['foo'] =='bar':
        intent = stripe.PaymentIntent.create(
            amount=100,
            currency='usd',
            metadata={'integration_check':'accept_a_payment'},)

        return JsonResponse({'client_secret':intent.client_secret})
    amount = request.session['payable']
    amount = amount * 100
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        metadata={'integration_check': 'accept_a_payment'},
        )
    print(intent)
    return JsonResponse({'client_secret':intent.client_secret})


#set the price that will be received later by payment method
def set_price(request):
    price = request.GET.get('mprice')
    if price == '1.00':
        price = 1
    price = int(price)
    request.session['payable'] = price
    request.session['foo'] = 'no_variable'
    return HttpResponse(str(price))


#save the price in the PaymentProgress model in order to track the progress of funds
def save_price(request):
    payable = request.session['payable']
    pf = PaymentProgress.objects.filter(id=1)
    if pf:
        pp = PaymentProgress.objects.get(id=1)
    else:
        pp = PaymentProgress.objects.create()
    pp.amount_paid = pp.amount_paid + payable
    pp.save()
    PaymentProgressAmount = pp.amount_paid
    fund = Funds.objects.latest('id')
    funding_required = fund.funds_required
    AllPaymentProgress = int(PaymentProgressAmount * 100 / funding_required)
    if AllPaymentProgress >= 99:
        pp.pebble_meter = True
        pp.save()
    return HttpResponse('ok') 



#make payment with stripe
def payment(request):
   if request.method =='POST':
    charge = stripe.Charge.create(amount=500, currency='usd',description='apito charge',source=request.POST.get('stripeToken'))
    print("Stripe Token: ",request.POST.get('stripeToken'))
    print("Charge: ",charge)
    return HttpResponse('Ok')





#redirect user to home page
def home(request):
    return redirect('home')




#retrieve pebble form input fields
def get_pebble_fields(request):
    fields_count = request.session['pebble_form_count']
    request.session['pebble_form_count'] = fields_count + 1


    PaymentProgressObject = PaymentProgress.objects.latest('id')
    PaymentProgressAmount = PaymentProgressObject.amount_paid
    fund = Funds.objects.latest('id')
    funding_required = fund.funds_required
    AllPaymentProgress = int(PaymentProgressAmount * 100 / funding_required)
    print("APP: ",AllPaymentProgress)
    if AllPaymentProgress >= 99:
        bleach = False #Random name
        remaining_pebbles = fund.limited_pebbles
        if fields_count >= remaining_pebbles:
            return HttpResponse('<p>no more pebbles available.</p>')

    return render(request,'pebble_form_input_fields.html',{'fields_count':fields_count})

#retrieve egift form input fields
def get_egift_fields(request):
    fields_count = request.session['egift_form_count']
    request.session['egift_form_count'] = fields_count + 1
    return render(request,'egift_form_input_fields.html',{'fields_count':fields_count})




#receive pebbles from the client side and save them
@csrf_exempt
def index(request):
    if request.method=='POST':
        try:
            order_no = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
            cnt = 0
            for key, value in request.FILES.items():
                file = value
                key_num_reg = re.search(r'\d+$', key)
                key_num = key_num_reg.group() if key_num_reg else None
                if key_num == None:
                    file_type = request.POST['file_type']
                    text = request.POST['text']
                else:
                    file_type_variable = 'file_type' + key_num
                    text_variable = 'text' + key_num
                    file_type = request.POST[file_type_variable]
                    text = request.POST[text_variable]
                file_model = FileModel.objects.create(file_type=file_type, text=text,file_here=file, order_no=order_no)
                cnt += 1
                print(file_model.id)
                print(file_model.order_no)

            #disable coupon
            cpn = request.POST.get('couponinput')
            cpni = CouponModel.objects.filter(coupon=cpn)
            print('cpni',cpni)
            if len(cpni) > 0:
                cpna = CouponModel.objects.get(coupon=cpn)
                print(cpna)
            pf = PaymentProgress.objects.filter(id=1)
            if pf:
                pp = PaymentProgress.objects.get(id=1)
                if pp.pebble_meter:
                    f= Funds.objects.latest('id')
                    lp = f.limited_pebbles
                    if cnt > lp:
                        new_lp = 0
                    else:
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
                from_email = 'admin@apebbleintheocean.com'
                to = em
                html_content = '<p>Hello there,</p><p>Here is the order number for the pebbles you uploaded through Apito:</p><p>{}</p><p>Keep this order number to be able to reference the pebbles you uploaded. You will also need this order number later on to find your pebbles when the time capsule is reopened.</p><p>On behalf of Apito, thank you for your contribution.<p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format(order_no)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content,"text/html")
                msg.send()
                print(msg)


            return HttpResponse(rsp)
        except:
            return HttpResponse('something bad happened')
    file_form = FileModelForm()
    return redirect('/')




#get extra data from the client side (pebble time, country, etc)
@csrf_exempt
def getextra(request):
    if request.method=='POST':
        idofform = request.POST.get('idoffileform')
        if not idofform: #id was used first but then replaced with order_no so changed id=idofform to order_no=idofform
            return render(request,'upload_success.html')

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
        ExtraInfo.objects.create(order_no=idofform, info=exinfo, country=excountry)
        return render(request,'upload_success.html')


def get_survey_result(request):
    if not request.user.is_superuser:
        return HttpResponse("denied")
    extras = ExtraInfo.objects.all()
    time_dic = {}
    country_dic = {}

    for e in extras:
        if e.info:
            if e.info in time_dic:
                get_info = time_dic[e.info]
                time_dic[e.info] = get_info + 1
            else:
                time_dic[e.info] = 1
        if e.country:
            if e.country in country_dic:
                get_country = country_dic[e.country]
                country_dic[e.country] = get_country + 1
            else:
                country_dic[e.country] = 1

    result = "<h3>Pebble Duration Survey Result</h3><b>"
    for key, val in time_dic.items():
        result += "<p>{}: {}</p>".format(key,val)
    result += "<br><h3>Country Survey Result</h3><br>"
    for key, val in country_dic.items():
        result += "<p>{}: {}</p>".format(key,val)

    return HttpResponse(result)







#calculate the price for the selected pebble items
def calculate_price(request):
    b = request.GET.get('lol')
    fileslist = b.split("xxxhumkohumhisaychuraloxxx")
    fileslist.pop()
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



#admin can use this point to create mass egifts 
def egifts_admin(request):
    if not request.user.is_superuser:
        return HttpResponse("error: not authorized")
    
    else:
        amount = request.GET.get('amount')
        if amount:
            amount = int(amount)
        qnt = request.GET.get('quantity')
        if qnt:
            qnt = int(qnt)

        if amount and qnt:
            if amount > 0 and qnt > 0:
                counter = 0
                codes = ""
                while counter < qnt:
                    cpn = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
                    cpn_obj = CouponModel.objects.create(amount=amount, coupon=cpn)
                    codes = codes + cpn + "\n"
                    counter +=1
                return HttpResponse(codes, content_type="text/plain")
                
        return render(request,'razi.html')
    

#check the validity of coupon
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
            cpn.delete()
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









#import modules

import zipfile
from io import BytesIO
import os
import shutil



#download all data
def file_download_url(request):
    if not request.user.is_superuser:
        return HttpResponse("denied")
    mr = settings.MEDIA_ROOT + 'apito_files'
    if not os.path.exists(mr):
        os.mkdir(mr)

    files = FileModel.objects.all()
    total_orders = []
    for file in files:
        if file.order_no in total_orders:
            pass
        else:
            total_orders.append(file.order_no)
    print(total_orders)
    for order in total_orders:
        file_objects = FileModel.objects.filter(order_no=order)
        cnt = 1
        order_dir = mr + '/' + str(order)
        if not os.path.exists(order_dir):
            os.mkdir(order_dir)
        for file in file_objects:
            file_here = file.file_here
            file_here_path = file_here.path
            if os.path.exists(file_here_path):
                pebble_dir = order_dir + '/pebble_' + str(cnt)
                if not os.path.exists(pebble_dir):
                    os.mkdir(pebble_dir)
                p = file_here.path.split('.')[1]
                new = pebble_dir + '/pebble_' + str(cnt) + '.' + p 
                shutil.copyfile(file_here.path,new)
                txt = file.text
                txt_file = pebble_dir + '/pebble_' + str(cnt) + '.txt'
                infile = open(txt_file,'w')
                infile.write(txt)
                infile.close()
            cnt +=1
    for ff in files:
        ff.delete()
    mm = settings.MEDIA_ROOT + 'file_content'
    shutil.rmtree(mm)
    shutil.make_archive(mr,'zip',mr)
    return redirect('/media/apito_files.zip')






#create coupon by receiving data from client side
@csrf_exempt
def create_coupon(request):
    if request.method=='POST':
        sender_email = request.POST.get('sender_email',None)
        sender_name = request.POST.get('sender_name',None)
        if sender_name:
            sender = sender_name
        elif sender_email:
            sender = sender_email
        else:
            sender = 'Someone'

        result_html = ""

        for key, val in request.POST.items():
            if key.startswith('amount'):
                amount = val
                key_num_reg = re.search(r'\d+$', key)
                key_num = key_num_reg.group() if key_num_reg else None
                if key_num == None:
                    receiver_email = request.POST['receiveremail1']
                    receiver_message = request.POST['receivermessage1']
                else:
                    key_num = int(key_num) + 1
                    key_num = str(key_num)
                    receiver_email_var = 'receiveremail' + key_num
                    receiver_email = request.POST.get(receiver_email_var,None)
                    receiver_message_var = 'receivermessage' + key_num
                    receiver_message = request.POST.get(receiver_message_var, None)
                coupon = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
                CouponModel.objects.create(amount=amount, coupon=coupon, receiver_email=receiver_email, msg_for_rcvr=receiver_message, sender_name=sender_name, sender_email=sender_email)
                if receiver_email:
                    subject = '{} has sent you an Apito eGift'.format(sender)
                    if receiver_message:
                        html_content = '<p>Hello there,</p><p>{} has sent you an apito eGift.</p><p>Code: {}</p><p>Amount: ${}</p><p>{}\'s message: {}</p><p>You can use the eGift to upload your pebbles through the Apito website, linked below:</p><p><a href="https://www.apebbleintheocean.com">www.apebbleintheocean.com</a></p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format(sender, coupon,amount, sender, receiver_message)
                    else:
                        html_content = '<p>Hello there,</p><p>{} has sent you an apito eGift.</p><p>Code: {}</p><p>Amount: ${}</p><p>You can use the eGift to upload your pebbles through the Apito website, linked below:</p><p><a href="https://www.apebbleintheocean.com">www.apebbleintheocean.com</a></p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'.format(sender, coupon,amount, sender)


                    from_email = 'admin@apebbleintheocean.com'
                    to = receiver_email
                    text_content = 'Apito eGift Notification'
                    msg = EmailMultiAlternatives(subject,text_content, from_email,[to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    result_html += "<p>Receiver: {} Coupon: {} Amount: ${}</p>".format(receiver_email,coupon, amount)
                else:
                    result_html +="<p>Coupon: {} Amount: ${}</p>".format(coupon, amount)

        if sender_email:
            subject = "Your Apito eGifts"
            html_content = '<p>Hello there,</p><p>Here are the Apito eGifts you purchased:</p>' + result_html + '<p>On behalf of Apito, thank you for your contribution.</p><br><p>Sincerely,</p><p>The Apito Team</p><br><p style="text-align: center;">Be a part of history.</p><p style="text-align: center;">Throw your pebble into the ocean</p><p style="text-align: center;"><img src="https://i.ibb.co/9YFKxSN/imageedit-8-3140283555.png" width="75" height="75"/></p>'
            from_email = 'admin@apebbleintheocean.com'
            to = sender_email
            text_content = 'Apito eGift Notification'
            msg = EmailMultiAlternatives(subject,text_content, from_email,[to])
            print(msg)
            msg.attach_alternative(html_content, "text/html")
            print('msg.send()',msg.send())
        return HttpResponse(result_html)

    return render(request,'coupon_success.html')




#show donation success page
def donation_success(request):
    return render(request, 'donation_success.html')


#serve this file in order to get validated by apple in order to use apple pay
def apple_pay_file(request):
    return redirect('/media/apple-developer-merchantid-domain-association')



#get total pebble count for video and iamge pebbles
def get_pebble_count(request):
    if not request.user.is_superuser:
        return HttpResponse("denied")
    
    ff = FileModel.objects.all()
    image_ext = ['png','jpg','jpeg','heic','gif']
    video_ext = ['avi','flv','wmv','mov','mp4','mkv']
    pic_p = 0
    vid_p = 0
    for f in ff:
        if f.file_here:
            p = f.file_here.path.split('.')[1]
            if p in image_ext:
                pic_p += 1
            elif p in video_ext:
                vid_p += 1
        if f.file_here1:
            p = f.file_here1.path.split('.')[1]
            if p in image_ext:
                pic_p += 1
            elif p in video_ext:
                vid_p += 1
        if f.file_here2:
            p = f.file_here2.path.split('.')[1]
            if p in image_ext:
                pic_p += 1
            elif p in video_ext:
                vid_p += 1
        if f.file_here3:
            p = f.file_here3.path.split('.')[1]
            if p in image_ext:
                pic_p += 1
            elif p in video_ext:
                vid_p += 1
        if f.file_here4:
            p = f.file_here4.path.split('.')[1]
            if p in image_ext:
                pic_p += 1
            elif p in video_ext:
                vid_p += 1
    resp_str = "Picture Pebbles Count: {}<br>Video Pebbles Count:{}".format(pic_p, vid_p)
    return HttpResponse(resp_str)