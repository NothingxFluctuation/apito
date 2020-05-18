from django.db import models
from django.utils import timezone

# Create your models here.


class VideoModel(models.Model):
	text = models.CharField(max_length=2000)
	video = models.FileField(upload_to='videos/',null=True, max_length = 400)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.video)



class ImageModel(models.Model):
	text = models.CharField(max_length=2000)
	image = models.FileField(upload_to='images/',null=True, max_length = 400)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.image)

ftype = [('im','Image'),('vid','Video')]

class FileModel(models.Model):
	file_type = models.CharField(max_length=50, choices=ftype, default='im', blank=True)
	text = models.TextField(max_length=4000, null=True, blank=True)
	file_here = models.FileField(upload_to='file_content/',null=True, blank=True,max_length=400)
	file_type1 = models.CharField(max_length=50, choices=ftype, default='im', blank=True)
	text1 = models.TextField(max_length=4000, null=True, blank=True)
	file_here1 = models.FileField(upload_to='file_content/', null=True, blank=True, max_length=400)
	file_type2 = models.CharField(max_length=50, choices=ftype, default='im', blank=True)
	text2 = models.TextField(max_length=4000, null=True, blank=True)
	file_here2 = models.FileField(upload_to='file_content/', null=True, blank=True, max_length=400)
	file_type3 = models.CharField(max_length=50, choices=ftype, default='im', blank=True)
	text3 = models.TextField(max_length=4000, null=True, blank=True)
	file_here3 = models.FileField(upload_to='file_content/', null=True, blank=True, max_length=400)
	file_type4 = models.CharField(max_length=50, choices=ftype, default='im', blank=True)
	text4 = models.TextField(max_length=4000, null=True, blank=True)
	file_here4 = models.FileField(upload_to='file_content/', null=True, blank=True, max_length=400)
	order_no = models.CharField(max_length=500,null=True, blank=True)
	created = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return str(self.file_here)

class ExtraInfo(models.Model):
	file = models.ForeignKey(FileModel, on_delete= models.CASCADE, related_name='file_extra')
	info = models.CharField(max_length=2000, null=True, blank=True)
	country = models.CharField(max_length=2000, null=True, blank=True)



class PaymentProgress(models.Model):
	amount_paid = models.IntegerField(default=0)
	pebble_meter = models.BooleanField(default=False)
	created = models.DateTimeField(default=timezone.now)


class Funds(models.Model):
	funds_required = models.IntegerField(default=0)
	limited_pebbles = models.IntegerField(default=0)
	remaining_pebbles = models.IntegerField(default=0)


class CouponModel(models.Model):
	amount = models.FloatField(max_length=100,blank=True, null=True)
	coupon = models.CharField(max_length=100, blank=True, null=True)
	#receiver_email = models.CharField(max_length=100, blank=True, null=True)
	#msg_for_rcvr = models.TextField(max_length=3000, blank=True, null=True)
	#sender_name = models.CharField(max_length=200, blank=True, null=True)
	#sender_email = models.CharField(max_length=200, blank=True,null=True)
	active = models.BooleanField(default=True)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.coupon


class ContactModel(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=254)
	message = models.TextField(max_length=2000)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.created