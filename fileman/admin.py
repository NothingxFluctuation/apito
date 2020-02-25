from django.contrib import admin
from fileman.models import VideoModel, ImageModel, FileModel, CouponModel
from django.http import HttpResponse

# Register your models here.

def download_all_files(ModelAdmin, request, queryset):
	response = HttpResponse(content_type='text/css')
	response['Content-Disposition'] = 'attachment; filename=teachermodel.zip'
	return response
download_all_files.short_description = u"Download All Files"



class VideoModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','video','created')
#admin.site.register(VideoModel, VideoModelAdmin)




class ImageModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','image','created')
#admin.site.register(ImageModel, ImageModelAdmin)

class FileModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','file_here','url','created')
	exclude = ('country','info')
	actions = [download_all_files,]
admin.site.register(FileModel, FileModelAdmin)


admin.site.register(CouponModel)