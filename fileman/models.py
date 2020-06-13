from django.db import models
from django.utils import timezone

# Create your models here.


#file types that will be accepted in models
ftype = [('im','Image'),('vid','Video')]


#create the model that will save received files
class FileModel(models.Model):
	file_type = models.CharField(max_length=50, choices=ftype, default='im', blank=True)
	text = models.TextField(max_length=4000, null=True, blank=True)
	file_here = models.FileField(upload_to='file_content/',null=True, blank=True,max_length=400)
	order_no = models.CharField(max_length=500,null=True, blank=True)
	created = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return str(self.file_here)


#model for extra information about pebbles
class ExtraInfo(models.Model):
	# file = models.ForeignKey(FileModel, on_delete= models.CASCADE, related_name='file_extra')
	order_no = models.CharField(max_length=2000, null=True, blank=True)
	info = models.CharField(max_length=2000, null=True, blank=True)
	country = models.CharField(max_length=2000, null=True, blank=True)


#model to save information about how much payments are being done
class PaymentProgress(models.Model):
	amount_paid = models.IntegerField(default=0)
	pebble_meter = models.BooleanField(default=False)
	created = models.DateTimeField(default=timezone.now)

#model to save information about funds collection
class Funds(models.Model):
	funds_required = models.IntegerField(default=0)
	limited_pebbles = models.IntegerField(default=0)
	remaining_pebbles = models.IntegerField(default=0)


#model to save coupon/egifts 
class CouponModel(models.Model):
	amount = models.FloatField(max_length=100,blank=True, null=True)
	coupon = models.CharField(max_length=100, blank=True, null=True)
	receiver_email = models.CharField(max_length=100, blank=True, null=True)
	msg_for_rcvr = models.TextField(max_length=3000, blank=True, null=True)
	sender_name = models.CharField(max_length=200, blank=True, null=True)
	sender_email = models.CharField(max_length=200, blank=True,null=True)
	active = models.BooleanField(default=True)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.coupon

