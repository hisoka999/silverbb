from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from board.models import Board,Thread
from backend.models import Theme,get_clean_text
from django.core.files.storage import FileSystemStorage
from django.conf import settings 
import datetime


fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0],base_url='/static/')  

def get_group(user):
    if user.is_anonymous():
        return auth.models.Group.objects.get(pk=2)
    else:
        return user.groups.all()[0]
class Rank(models.Model):
    name  = models.CharField(max_length=30)
    """ path to the image on the webserver """
    image = models.CharField(max_length=300)
    """ says how many images should be displayed """
    times = models.IntegerField(default=0)
    """ number of posts required for this rank to appear """
    posts = models.IntegerField(default=0)
    """ accociated group for this rank """
    group = models.ForeignKey(auth.models.Group,null=True)
    
    def make_list(self):
        """ returns a list from 0 to times """
        return xrange(0,self.times,1)

class UserProfile(models.Model):
    """
    Stores a single user profile, related to :model:`auth.User` and
    :model:`board.Thread`.

    """
    user       = models.ForeignKey(User, unique=True,help_text="The current user associated with this profile")
    posts      = models.IntegerField(default=0)
    threads    = models.IntegerField(default=0)
    banned     = models.BooleanField(default=False)
    website    = models.URLField(blank=True)
    icq        = models.CharField(max_length=20,blank=True)
    skype      = models.CharField(max_length=40,blank=True)
    # holds the filename for the avatar of the user
    avatar     = models.ImageField(blank=True,storage=fs,upload_to='avatars')
    activate   = models.CharField(blank=False, max_length=32)
    theme      = models.ForeignKey(Theme,blank=True,default=False,null=True)
    show_email = models.BooleanField(default=False)
    show_name  = models.BooleanField(default=False)
    send_mail  = models.BooleanField(default=False)
    signature  = models.TextField(blank=True)

    def get_cleaned_signature(self):
        return get_clean_text(self.signature)
    
    def get_rank(self):
        return Rank.objects.filter(posts__lte=self.posts).get(group=self.user.groups.all()[0])

    def get_posts_per_day(self):
            diff = datetime.datetime.now()-self.user.date_joined
            return float(self.posts)/float(diff.days)

class UserSession(models.Model):
    user = models.ForeignKey(User,null=True,blank=True)
    session_key = models.CharField(max_length = 100)
    board = models.ForeignKey(Board,blank=True,null=True)
    thread = models.ForeignKey(Thread,blank=True,null=True)
    time = models.DateTimeField(auto_now=True)
    captcha = models.CharField(max_length= 20,blank=True,null=True)