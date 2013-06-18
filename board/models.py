from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
from silverbb.backend.models import get_clean_text
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.shortcuts import render


class Board(models.Model):
    name        = models.CharField(max_length=40)
    description = models.TextField(null=True,blank=True)
    parent      = models.ForeignKey('self',null=True,blank=True)
    threads     = models.IntegerField(default=0)
    posts       = models.IntegerField(default=0)
    moderators  = models.ManyToManyField(User,blank=True)
    rights      = models.ManyToManyField(auth.models.Group,through='BoardRights')
    
    def get_name_for_url(self):
        return self.name.replace(' ','_').lower()
        
    
    def get_children(self):
        return Board.objects.filter(parent=self.pk)
    
    def get_path(self):
        print self.parent
        if self.parent is None:
            return '<a href="'+reverse('board.views.show_board',args=[self.id,self.get_name_for_url()])+'">'+self.name+'</a>'
        else:
            return self.parent.get_path()+"&raquo;"+'<a href="'+reverse('board.views.show_board',args=[self.id,self.get_name_for_url()])+'">'+self.name+'</a>'
    
    def __unicode__(self):
        return self.name
    
    def list(self,parent = 1):
        ret = ""
        for b in self.board_set.all():
            ret = b.list(parent+1)
        return render_to_string('board/list.html',{'board':self,'list':ret,'parent':'&nbsp;'*parent*2})

class BoardRights(models.Model):
    board = models.ForeignKey(Board)
    group = models.ForeignKey(auth.models.Group)
    can_view   = models.BooleanField()
    can_post   = models.BooleanField()
    can_thread = models.BooleanField()
    
    
class Thread(models.Model):
    name   = models.CharField(max_length=100)
    posts  = models.IntegerField(default=0)
    author = models.ForeignKey(User,null=True,blank=True)
    guest  = models.CharField(max_length=100,null=True,blank=True)
    board  = models.ForeignKey(Board)
    moved_from = models.ForeignKey(Board,blank=True,null=True,related_name='moved_from')
    closed = models.BooleanField(blank=True,default=False)
    views  = models.IntegerField(default=0)
    
    def get_url_name(self):
        return self.name.replace(' ','_')
    
    def get_last_post(self):
        return self.post_set.latest('time_created')
    
    def get_first_post(self):
        return self.post_set.order_by('time_created')[0]
    
    def __unicode__(self):
        return self.name
    
class Post(models.Model):
    name         = models.CharField(max_length=100)
    thread       = models.ForeignKey(Thread)
    time_created = models.DateTimeField(auto_now=True)
    time_edited  = models.DateTimeField(null=True)
    text         = models.TextField()
    user         = models.ForeignKey(User,null=True)
    guest_name   = models.CharField(max_length=100,null=True,blank=True)
    smilies      = models.BooleanField()
    use_html     = models.BooleanField()
    
    def get_cleaned_post(self):
        return get_clean_text(self.text)
        
    
    def __unicode__(self):
        return self.name
