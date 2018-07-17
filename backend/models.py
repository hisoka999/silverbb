from django.db import models
from django.conf import settings
#from functions import get_path
import re
from django.db.models.query_utils import Q

import functools

def memoize(method):
    @functools.wraps(method)
    def memoizer(*args, **kwargs):
        method._cache = getattr(method, '_cache', {})
        key = args
        if key not in method._cache:
            method._cache[key] = method(*args, **kwargs)
        return method._cache[key]
    return memoizer

class BBCode(models.Model):
    name    = models.CharField(max_length=10)
    search  = models.CharField(max_length=200)
    replace = models.CharField(max_length=200)
    
class Smilie(models.Model):
    code        = models.CharField(max_length=10)
    smile_url   = models.CharField(max_length=40)
    emoticon    = models.CharField(max_length=20)

class Theme(models.Model):
    name        = models.CharField(max_length=100)
    version     = models.IntegerField(default=1)
    folder      = models.CharField(max_length=200,default='',null=True,blank=True)
    default     = models.BooleanField(default=False)
    
    def update_default(self):
        if (self.default==True):
            Theme.objects.filter(~Q(pk=self.id)).update(default=False)
    
    def save(self):
        self.update_default()
        super(Theme,self).save()
    
    def __unicode__(self):
        return self.name

@memoize
def get_path(user=None):
    if user == None or user.is_authenticated() == False:
        return Theme.objects.filter(default=True)[0].folder
    else:
        return user.get_profile().theme.folder

@memoize
def get_bbcodes():
    return BBCode.objects.all()

@memoize
def get_smilies():
    return Smilie.objects.all()


def get_clean_text(text):
    temp = text
    objs=get_bbcodes()
    for obj in objs:
        temp= re.sub(obj.search,obj.replace,temp,flags=re.MULTILINE)

    smilies = get_smilies()
    for obj1 in smilies:
        temp = re.sub(re.escape(obj1.code),'<img src="'+settings.STATIC_URL+get_path()+'images/smiles/'+obj1.smile_url+'" />',temp)
    return temp