from django.contrib import admin
from fileman.models import FileModel, CouponModel, PaymentProgress, Funds
from django.http import HttpResponse


# Register your models here.



class FileModelAdmin(admin.ModelAdmin):
	list_display = ('order_no','text','file_here','created')
	search_fields = ['order_no',]
#register file model	
admin.site.register(FileModel, FileModelAdmin)



class PaymentProgressAdmin(admin.ModelAdmin):
	list_display = ('amount_paid','pebble_meter')
#register payment progress model
admin.site.register(PaymentProgress, PaymentProgressAdmin)


class FundsAdmin(admin.ModelAdmin):
	list_display = ('funds_required','limited_pebbles')

#register funds model
admin.site.register(Funds, FundsAdmin)


class CouponModelAdmin(admin.ModelAdmin):
	list_display = ('coupon','amount','receiver_email','msg_for_rcvr','sender_name','sender_email')
	search_fields = ['coupon']
#register coupon model
admin.site.register(CouponModel, CouponModelAdmin)