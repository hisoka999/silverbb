# Create your views here.
from functions import render_to_response
from django.template import RequestContext

def show_css(request,css_file1):
    #print 'css/'+css_file+'.css'
    return render_to_response('css/'+css_file1+'.css',{},context_instance=RequestContext(request),mimetype="text/css")


def show404(request):
    """
    404 error handler.

    Templates: `404.html`
    Context: None
    """
    return render_to_response('404.html',
        context_instance = RequestContext(request)
    )