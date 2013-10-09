from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=40)
    usage = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name

class Entry(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)
    
    def __unicode__(self):
        return self.title
    
    def get_comments(self,user):
        if (user.is_staff):
            return self.comment_set.order_by('-created_at')
        else:
            return self.comment_set.filter(activated=True).order_by('-created_at')
    
    
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=20,blank = True,null=True)
    user_mail = models.EmailField(blank = True,null=True)
    activated = models.BooleanField(default=False)
    entry = models.ForeignKey(Entry)
#    user = models.ForeignKey(User,blank = True,null=True)