from django.contrib import admin
from fileman.models import VideoModel, ImageModel, FileModel, CouponModel, PaymentProgress, Funds
from django.http import HttpResponse


# Register your models here.



class VideoModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','video','created')
#admin.site.register(VideoModel, VideoModelAdmin)




class ImageModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','image','created')
#admin.site.register(ImageModel, ImageModelAdmin)

class FileModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','file_here','created')
	
admin.site.register(FileModel, FileModelAdmin)



class PaymentProgressAdmin(admin.ModelAdmin):
	list_display = ('amount_paid','pebble_meter')
admin.site.register(PaymentProgress, PaymentProgressAdmin)


class FundsAdmin(admin.ModelAdmin):
	list_display = ('funds_required','limited_pebbles')
admin.site.register(Funds, FundsAdmin)


class CouponModelAdmin(admin.ModelAdmin):
	list_display = ('coupon','amount')
admin.site.register(CouponModel, CouponModelAdmin)