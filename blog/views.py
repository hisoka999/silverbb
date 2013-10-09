# Create your views here.
from models import *
from forms import CommentForm
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.paginator import Paginator
from silverbb.backend.functions import render_to_response
from django.contrib import messages


def index(request,page=1):
    if (page < 1):
        page = 1
    entries = Entry.objects.order_by('-created_at')
    pages = Paginator(entries,10)
    
    return render_to_response('blog/index.html',{'entries':pages.page(page)},context_instance=RequestContext(request))



def blog_post(request,entry_id):
    entry = Entry.objects.get(pk=entry_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            post = comment_form.save(False)
            post.entry = entry
            post.save()
            messages.add_message(request, messages.INFO, 'comment successfully added.')
    else:        
        comment_form = CommentForm()
    return render_to_response('blog/show.html',{'entry':entry,'form':comment_form},context_instance=RequestContext(request))

def tag_search(request,tag_name,page=1):
    tag = Tag.objects.get(name=tag_name)
    entries = Entry.objects.filter(tags__name=tag_name).order_by('-created_at')
    if (page < 1):
        page = 1
    pages = Paginator(entries,10)
    return render_to_response('blog/tag.html',{'entries':pages,'tag':tag},context_instance=RequestContext(request))