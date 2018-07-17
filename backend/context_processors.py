'''
Created on 21.05.2011

@author: stefan
'''
import version as ver
from django.conf import settings
from functions import get_path
from django.contrib.sites.shortcuts import get_current_site
from models import Smilie
from functions import memoize

@memoize
def theme_path(request):
    return {'STATIC_THEME':settings.STATIC_URL+get_path(request.user)
            ,'BASE_PATH':get_path(request.user)+'base.html'
            ,'CURRENT_SITE':get_current_site(request)
            ,'THEME_PATH':get_path(request.user)
            ,'smilies':Smilie.objects.all()}

def version(request):
    return {'version':ver.sbb_version,'revision':ver.revision()}