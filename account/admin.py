from django.contrib import admin
from .models import Profile,FileDownload,File
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display =['user','photo']
    
    
    
admin.site.register(File)
admin.site.register(FileDownload)