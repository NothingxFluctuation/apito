from django.contrib import admin
from fileman.models import VideoModel, ImageModel, FileModel

# Register your models here.


class VideoModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','video','created')
#admin.site.register(VideoModel, VideoModelAdmin)




class ImageModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','image','created')
#admin.site.register(ImageModel, ImageModelAdmin)

class FileModelAdmin(admin.ModelAdmin):
	list_display = ('id','text','file_here','url','created')
admin.site.register(FileModel, FileModelAdmin)