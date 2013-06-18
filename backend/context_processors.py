'''
Created on 21.05.2011

@author: stefan
'''
from silverbb import version as ver
from django.conf import settings
from functions import get_path
from django.contrib.sites.models import get_current_site

def theme_path(request):
    return {'STATIC_THEME':settings.STATIC_URL+get_path(request.user),'BASE_PATH':get_path(request.user)+'base.html','CURRENT_SITE':get_current_site(request),'THEME_PATH':get_path(request.user)}

def version(request):
    return {'version':ver.sbb_version,'revision':ver.revision()}