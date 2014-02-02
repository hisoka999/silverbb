from models import Category,Topic
from backend.functions import render_to_response
from django.template.context import RequestContext
def index(request):
    cats = Category.objects.all().order_by('-name')
    return render_to_response('faq/index.html',{'cats':cats},context_instance=RequestContext(request))

def topic(request,topic_id):
    try:
        topic_id = int(topic_id)
    except ValueError:
        topic_id=1
    
    topic = Topic.objects.get(pk=topic_id)
    return render_to_response('faq/topic.html',{'topic':topic},context_instance=RequestContext(request))