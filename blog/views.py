from collections import namedtuple

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import redirect
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import gettext as _

from backend.functions import render_to_response
from blog.forms import CommentForm, EntryForm
from blog.models import Entry, Tag


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def index(request,page=1):
    if (page < 1):
        page = 1
    entries = Entry.objects.order_by('-created_at')
    pages = Paginator(entries,10)
    
    Entry.objects.values('created_at')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT YEAR(created_at) 'year',MONTHNAME(created_at) 'month',MONTH(created_at) 'month_num' FROM `blog_entry` ORDER BY 1 DESC,2 DESC")
        dates = namedtuplefetchall(cursor)
    
    return render_to_response('blog/index.html',{'entries':pages.page(page),'dates':dates},context_instance=RequestContext(request))



def blog_post(request,entry_id):
    entry = Entry.objects.get(pk=entry_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            post = comment_form.save(False)
            post.entry = entry
            post.save()
            messages.add_message(request, messages.INFO, _('comment successfully added.'))
    else:        
        comment_form = CommentForm()
    return render_to_response('blog/show.html',{'entry':entry,'form':comment_form,'comments':entry.get_comments(request.user)},context_instance=RequestContext(request))

def tag_search(request,tag_name,page=1):
    tag = Tag.objects.get(name=tag_name)
    entries = Entry.objects.filter(tags__name=tag_name).order_by('-created_at')
    if (page < 1):
        page = 1
    pages = Paginator(entries,10)
    return render_to_response('blog/tag.html',{'entries':pages.page(page),'tag':tag},context_instance=RequestContext(request))

def archive(request,year,month,page=1):
    entries = Entry.objects.filter(created_at__year=year,
                                   created_at__month=month).order_by('-created_at')
    if (page < 1):
        page = 1
    pages = Paginator(entries,10)                                   
    return render_to_response('blog/archive.html',{'entries':pages.page(page),'month':month,'year':year},context_instance=RequestContext(request))


@permission_required('blog.can_add_entry', login_url='/user/login/')
def create_entry(request):
    form = EntryForm()
    if (request.method == 'POST'):
        form = EntryForm(data=request.POST)

        if (form.is_valid()):
            entry = form.save(False)

            entry.user = request.user
            entry.save()

            return redirect(reverse('blog.views.blog_post', args=[entry.id]))

    return render_to_response('blog/create_entry.html', {'form': form},
                              context_instance=RequestContext(request))
