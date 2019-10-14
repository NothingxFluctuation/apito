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
	file_type = models.CharField(max_length=50, choices=ftype, default='im')
	text = models.TextField(max_length=3000)
	file_here = models.FileField(upload_to='file_content/',null=True, max_length=400)
	created = models.DateTimeField(default=timezone.now)
	url = models.CharField(max_length=2000, null=True, blank = True)
	info = models.CharField(max_length=2000, null=True, blank=True)
	country = models.CharField(max_length=2000, null=True, blank=True)


	def __str__(self):
		return str(self.file_here)


class CouponModel(models.Model):
	coupon = models.CharField(max_length=100, blank=True, null=True)
	receiver_email = models.CharField(max_length=100, blank=True, null=True)
	msg_for_rcvr = models.TextField(max_length=3000, blank=True, null=True)
	sender_name = models.CharField(max_length=200, blank=True, null=True)
	sender_email = models.CharField(max_length=200)
	active = models.BooleanField(default=True)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.sender_email


class ContactModel(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=254)
	message = models.TextField(max_length=2000)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.created