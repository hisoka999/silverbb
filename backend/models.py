from django.db import models
from django.conf import settings
#from functions import get_path

import re

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
    
    def __unicode__(self):
        return self.name

def get_path(user=None):
    if user == None or user.is_authenticated() == False:
        return Theme.objects.filter(default=True)[0].folder
    else:
        return user.get_profile().theme.folder

def get_clean_text(text):
    temp = text
    objs=BBCode.objects.all()
    for obj in objs:
        temp= re.sub(obj.search,obj.replace,temp,flags=re.MULTILINE)

    smilies = Smilie.objects.all()
    for obj1 in smilies:
        temp = re.sub(re.escape(obj1.code),'<img src="'+settings.STATIC_URL+get_path()+'images/smiles/'+obj1.smile_url+'" />',temp)
    return temp