'''
Created on 24.12.2011

@author: stefan
'''
from models import BBCode,Smilie,Theme
from django.contrib import admin

class SmilieAdmin(admin.ModelAdmin):
    list_display = ['emoticon','code']

class BBCodeAdmin(admin.ModelAdmin):
    list_display = ['name','search','replace']

class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name','version','folder']

admin.site.register(Theme,ThemeAdmin)
admin.site.register(Smilie,SmilieAdmin)
admin.site.register(BBCode,BBCodeAdmin)