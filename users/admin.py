'''
Created on 24.12.2011

@author: stefan
'''
from models import *
from django.contrib import admin

class RankAdmin(admin.ModelAdmin):
    list_display = ['name','posts','group']
admin.site.register(Rank,RankAdmin)