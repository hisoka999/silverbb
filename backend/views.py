# Create your views here.
from functions import render_to_response
from django.template import RequestContext

def show_css(request,css_file1):
    #print 'css/'+css_file+'.css'
    return render_to_response('css/'+css_file1+'.css',{},context_instance=RequestContext(request),mimetype="text/css")