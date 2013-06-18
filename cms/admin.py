from django.contrib import admin
from models import *

class ImageInline(admin.TabularInline):
    model = Image

class DownloadAdmin(admin.ModelAdmin):
    list_display = ['name','category','count','visible']

class DownloadCatAdmin(admin.ModelAdmin):
    list_display = ['name','parent','visible']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','time']

class PageAdmin(admin.ModelAdmin):
    list_display = ['title']

class GalleryAdmin(admin.ModelAdmin):
    list_display = ['name','parent','show']
    inlines = [
        ImageInline,
    ]

class PageInline(admin.TabularInline):
    model = Topic.pages.through
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [
        PageInline,
    ]    

class MenuAdmin(admin.ModelAdmin):
    list_display = ['title','external_link','parent']
admin.site.register(NewsItem,NewsAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(MenuItem,MenuAdmin)
admin.site.register(DownloadCategory,DownloadCatAdmin)
admin.site.register(Download,DownloadAdmin)