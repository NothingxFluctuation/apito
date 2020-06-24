from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import fileman.views as fv
from django.conf.urls import url,include


#url configurations for the whole site
urlpatterns = [

	path('', fv.home, name='main'),
    path('success/', fv.getextra, name='getextra'),
    path('coupon/',fv.check_coupon, name='check_coupon'),
    path('create_coupon/',fv.create_coupon, name='create_coupon'),
    path('product/', fv.index, name='product'),
    path('get_pebble_fields/',fv.get_pebble_fields, name='get_pebble_fields'),
    path('get_egift_fields/', fv.get_egift_fields, name='get_egift_fields'),
    path('home/', fv.main, name='home'),
    path('faq/', fv.faq, name='thisabout'),
    path('terms-and-conditions/', fv.terms, name='t'),
    path('calculate_price/',fv.calculate_price, name='calculate_price'),
    path('payment/', fv.payment, name='payment'),
    path('secret/', fv.secret, name='secret'),
    path('set_price/', fv.set_price, name='set_price'),
    path('save_price/', fv.save_price, name='save_price'),
    path('get_pebble_count/', fv.get_pebble_count, name='get_pebble_count'),
    path('get_survey_result/', fv.get_survey_result, name='get_survey_result'),
    path('egifts_admin/', fv.egifts_admin, name="egifts_admin"),
    path('file_download_url/',fv.file_download_url, name='file_download_url'),
    path('.well-known/apple-developer-merchantid-domain-association/', fv.apple_pay_file,name='apple_pay_file'),
    path('donation_success/', fv.donation_success, name='donation_success'),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)