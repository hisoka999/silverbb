from models import Theme
from django.shortcuts import render_to_response as r_t_r
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
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

@memoize
def get_path(user=None):
    if user == None or user.is_authenticated() == False:
        return Theme.objects.get(default=True).folder
    else:
        return user.profile.theme.folder


def render_to_response(page,context=None,context_instance=None,mimetype=None): 
    
    template_name=get_path(context_instance.request.user)+page
    if mimetype == None:
        return render(context_instance.request,template_name,context)
    else:
        return r_t_r(get_path(context_instance.request.user)+page,context,context_instance,content_type=mimetype)