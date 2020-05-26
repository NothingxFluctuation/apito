"""apito URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import fileman.views as fv



urlpatterns = [

	path('', fv.main, name='main'),
    path('pa/',fv.pp, name='pp'),
	path('product/',fv.index, name='product'),
    path('success/', fv.getextra, name='getextra'),
    path('aja/',fv.aja, name='aja'),
    path('coupon/',fv.check_coupon, name='check_coupon'),
    path('create_coupon/',fv.create_coupon, name='create_coupon'),

    path('home/', fv.m, name='home'),
    path('faq/', fv.thisabout, name='thisabout'),
    path('us/',fv.us, name='us'),
    path('cntct/',fv.cntct, name='cntct'),
    path('p/', fv.p, name='p'),
    path('cpn/', fv.cpn, name='cpn'),
    path('terms-and-conditions/', fv.t, name='t'),
    path('calculate_price/',fv.calculate_price, name='calculate_price'),
    path('payment/', fv.payment, name='payment'),
    path('braintree_payment/', fv.braintree_payment, name='braintree_payment'),
    path('secret/', fv.secret, name='secret'),
    path('set_price/', fv.set_price, name='set_price'),
    path('save_price/', fv.save_price, name='save_price'),
    path('get_pebble_count/', fv.get_pebble_count, name='get_pebble_count'),

    path('egifts_admin/', fv.egifts_admin, name="egifts_admin"),

    path('download_all_files/',fv.download_all_files, name='download_all_files'),
    path('file_download_url/',fv.file_download_url, name='file_download_url'),
    path('download_csv/', fv.download_csv, name='download_csv'),
    path('.well-known/apple-developer-merchantid-domain-association/', fv.oh_my_apple,name='oh_my_apple'),

    path('donation_success/', fv.donation_success, name='donation_success'),


    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)