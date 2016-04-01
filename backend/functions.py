from models import Theme
from django.shortcuts import render_to_response as r_t_r
from django.shortcuts import render

def get_path(user=None):
    if user == None or user.is_authenticated() == False:
        return Theme.objects.filter(default=True)[0].folder
    else:
        return user.profile.theme.folder


def render_to_response(page,context=None,context_instance=None,mimetype=None):
    print context_instance.request.user
    print get_path(context_instance.get('user'))
    
    if mimetype == None:
        return r_t_r(get_path(context_instance.request.user)+page,context,context_instance)
    else:
        return r_t_r(get_path(context_instance.request.user)+page,context,context_instance,content_type=mimetype)