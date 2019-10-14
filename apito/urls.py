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
	path('product/',fv.index, name='product'),
    path('aja/',fv.aja, name='aja'),
    path('coupon/',fv.check_coupon, name='check_coupon'),
    path('create_coupon/',fv.create_coupon, name='create_coupon'),
    path('dwnid/', fv.file_download, name='file_download'),

    path('contact/', fv.contact, name='contact'),


    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)