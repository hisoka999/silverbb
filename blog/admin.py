'''
Created on 25.03.2013

@author: stefan
'''
from django.contrib import admin
from blog.models import Comment,Entry,Tag

class TagInline(admin.StackedInline):
    model = Entry.tags.through

class TagAdmin(admin.ModelAdmin):
    exclude = ('usage',)

class EntryAdmin(admin.ModelAdmin):
    list_display = ['title','created_at']
    inlines = [
        TagInline,
    ]
    exclude = ('tags','user')
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class CommentAdmin(admin.ModelAdmin):
    list_display = ['entry','user_name','user_mail','activated']
    
    def make_activated(self, request, queryset):
        rows_updated = queryset.update(activated=True)
        if rows_updated == 1:
            message_bit = "1 comment was"
        else:
            message_bit = "%s comments were" % rows_updated
        self.message_user(request, "%s successfully marked as activated." % message_bit)
    make_activated.short_description = "Mark as activated"
    actions = [make_activated]


admin.site.register(Entry,EntryAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Tag,TagAdmin)