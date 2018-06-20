from models import Theme
from django.shortcuts import render_to_response as r_t_r
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from models import Smilie
from django.template import RequestContext
from django.template.loader import get_template
from templatetags.cssfilter import *

def get_path(user=None):
    if user == None or user.is_authenticated() == False:
        return Theme.objects.filter(default=True)[0].folder
    else:
        return user.profile.theme.folder


def render_to_response(page,context=None,context_instance=None,mimetype=None): 
    
    template_name=get_path(context_instance.request.user)+page
    if mimetype == None:
        
        render
        
        return render(context_instance.request,template_name,context)
    else:
        return r_t_r(get_path(context_instance.request.user)+page,context,context_instance,content_type=mimetype)