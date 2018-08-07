'''
Created on 24.12.2011

@author: stefan
'''
from board.models import *
from django.contrib import admin


class BoardRightsInline(admin.TabularInline):
    model = BoardRights

class BoardAdmin(admin.ModelAdmin):
    inlines = [
        BoardRightsInline,
    ]
    list_display = ('name','parent')

class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    list_display = ('name','closed','author','board')
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('name','thread','user')    
admin.site.register(Board,BoardAdmin)
##admin.site.register(BoardRights)
admin.site.register(Thread,ThreadAdmin)
admin.site.register(Post,PostAdmin)