from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib import auth, messages
from django.db.models import Q
from models import Board,Thread,Post
from users.models import UserSession,get_group
from django.core.paginator import Paginator
from backend.models import BBCode, Smilie
from forms import *
from django.http import Http404,HttpResponseForbidden
from datetime import datetime
from board.models import BoardRights
from django.contrib.admin.views.decorators import staff_member_required
from django.core import urlresolvers
from backend.functions import render_to_response
from django.db.models import Q
from django.db.models.aggregates import Count
from board.models import Track
import traceback
import sys

def index(request):
    try:
        group = request.user.groups.all()[0]
    except:
        group = auth.models.Group.objects.get(name='Gast')
    boards = Board.objects.filter(parent=None,boardrights__group=group,boardrights__can_view=True)
    
    #load statistic data (users online)
    users = UserSession.objects.filter(user__gt=0)
    guest_count = UserSession.objects.filter(Q(user=0)|Q(user__isnull=True)).count()
    #load base stats
    all_user = auth.models.User.objects.count()
    all_threads = Thread.objects.count()
    all_posts = Post.objects.count()
    last_user = auth.models.User.objects.latest('date_joined')
    groups = auth.models.Group.objects.annotate(perm_count=Count('permissions')).filter(perm_count__gt=0)
    return render_to_response('index.html',
        {'boards':boards
         ,'users':users
         ,'groups':groups
         ,'guest_count':guest_count
         ,'all_user':all_user
         ,'all_threads':all_threads
         ,'all_posts':all_posts
         ,'last_user':last_user},context_instance=RequestContext(request))

def mark_read(request,board_id,display=True):
    if (request.user.id != None):
        track,created = Track.objects.get_or_create(board_id=board_id,user_id = request.user.id,defaults={'marked': datetime.now()})
        if (created):
            print "board_id = %d"%(board_id)
        track.marked = datetime.now()
        track.save()
    if (display):
        None ## redirect 

def show_board(request,board_id,board_name=""):

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        group = request.user.groups.all()[0]
    except:
        group = auth.models.Group.objects.get(name='Gast')    
    board = Board.objects.get(pk=board_id)
    boards = Board.objects.filter(parent=None,boardrights__group=group,boardrights__can_view=True)
    rights = BoardRights.objects.get(board= board_id,group=get_group(request.user))
    
    if rights.can_view:
        threads = Thread.objects.raw('''SELECT t.`id`,`closed`,`moved_from_id`,`board_id`,`author_id`,`posts`,t.`name`, max(p.time_created) time
            FROM  `board_thread` t,  `board_post` p
            WHERE t.id = p.thread_id
            AND  (`board_id` =%s
            OR `moved_from_id` =%s)
            GROUP BY t.`id`,`closed`,`moved_from_id`,`board_id`,`author_id`,`posts`,t.`name`
            ORDER BY max(p.time_created) DESC
        ''',[board_id,board_id])
        pages = Paginator(list(threads), 10)
        return render_to_response('board.html',{'board':board,'threads':pages.page(page),'rights':rights,'boards':boards},context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden

def show_thread(request,thread_id,thread_name=""):
    try:
        thread = Thread.objects.get(pk=thread_id)
    except:
        raise Http404
    rights = BoardRights.objects.get(board= thread.board_id,group=get_group(request.user))
    mod_form = ThreadModForm()
    try:
        group = request.user.groups.all()[0]
    except:
        group = auth.models.Group.objects.get(name='Gast')
    boards = Board.objects.filter(parent=None,boardrights__group=group,boardrights__can_view=True)
    page = 1
    try:
        page = int(request.GET.get('page','1'))
    except Exception,e:
        page = 1
    #mod_form.initial = 
    if rights.can_view:
        thread.views = thread.views+1
        thread.save()
        _posts = Post.objects.filter(thread=thread_id)
        posts = Paginator(_posts,10)
        ppage = posts.page(page)
        
        mark_read(request, thread.board_id, False)
        return render_to_response('thread.html',{'thread':thread,
                                                 't_posts':ppage,
                                                 'rights':rights,
                                                 'moderation':mod_form,
                                                 'boards':boards}
                                  ,context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden()

def create_post(request,thread_id):
    can_post = False
    #try:
    thread = Thread.objects.get(pk=thread_id)
    groups = []
    if (request.user.id is not None):
        groups =  request.user.groups.all()
    else:
        group = auth.models.Group.objects.get(name='Gast')
        groups.append(group)
    for right in thread.board.boardrights_set.all():
        if right.group in groups and right.can_post:
            can_post = True
    if not can_post:
        return HttpResponseForbidden()
    #except:
    #    raise Http404
    quote_id = request.GET.get('quote')
    if (request.method == "GET"):
        name = "Re: "+thread.name
        options = {'name':name,}
        if (quote_id):
            quote = Post.objects.get(pk = quote_id)
            print quote.text
            options['text'] ="[quote]%s[/quote]"%( quote.text)
        if (request.user.id is None):
            f_post = PostGuestForm(initial=options)
        else:
            f_post = PostForm(initial=options)
    else:
        if 'preview' in request.POST:
            # show a preview
            f_post = PostForm(data=request.POST)
            post = f_post.save(commit=False)
            if(f_post.is_valid()):          
                return render_to_response('create_post.html',{'f_post':f_post,'thread_id':thread_id,'preview':True,'preview_post':post},context_instance=RequestContext(request))
        else:
            if (request.user.id is None):
                f_post = PostGuestForm(request.POST)
            else:
                f_post = PostForm(request.POST)
            if(f_post.is_valid()):
                thread = Thread.objects.get(pk=thread_id)
                post = f_post.save(commit=False)
                post.thread = thread
                if (request.user.id is not None):
                    post.user = request.user
                post.save()
                thread.posts = thread.posts+1
                thread.save()
                #board=Board.objects.get()
                thread.board.posts = thread.board.posts + 1
                thread.board.save()
                if (request.user.id is not None):
                    profile = request.user.get_profile() 
                    profile.posts=profile.posts+1
                    profile.save()
                return render_to_response('create_thread_success.html',{'thread':thread,},context_instance=RequestContext(request))
    return render_to_response('create_post.html',{'f_post':f_post,'thread_id':thread_id},context_instance=RequestContext(request))

def edit_post(request,post_id):
    if request.method =='POST':
        if 'preview' in request.POST:
            # show a preview
            post = Post.objects.get(pk=post_id)
            if (post.user == request.user):
                # show the edit template
                f_post = PostForm(instance=post,data=request.POST)
                post = f_post.save(commit=False)             
                return render_to_response('edit_post.html',{'f_post':f_post,'post_id':post_id,'preview':True,'post':post},context_instance=RequestContext(request))
        else:
            post = Post.objects.get(pk=post_id)
            if (post.user == request.user):
                # show the edit template
                f_post = PostForm(instance=post,data=request.POST)            
                p=f_post.save(commit=False)
                p.time_edited = datetime.now()
                p.save()
                messages.add_message(request, messages.INFO, 'This reply was successfully edited.')
                return redirect(urlresolvers.reverse('board.views.show_thread',args=[p.thread.id,p.thread.get_url_name()]))
    try:
        post = Post.objects.get(pk=post_id)
        if (post.user == request.user or request.user.is_staff):
            # show the edit template
            html_file = "edit_post.html"
            f_post = PostForm(instance=post)
            if (request.is_ajax()):
                html_file = "edit_post_ajax.html"
                
            return render_to_response(html_file,{'f_post':f_post,'post_id':post_id},context_instance=RequestContext(request))
        else:
            messages.add_message(request, messages.ERROR, 'You are not allowed to edit this post.')
            return redirect(urlresolvers.reverse('board.views.show_thread',args=[p.thread.id,p.thread.get_url_name()]))
    except Exception as e:
        #return a 404 page
        #traceback.print_stack(e)
        traceback.print_exc(file=sys.stdout)
        print e
        raise Http404


def create_thread(request,board_id):
    """
    Display an new thread form or success page

    **Context**

    ``RequestContext``

    ``thread``
        An instance of :model:`board.Thread`.

    **Template:**

    :template:`create_thread_success.html`
    :template:`create_thread.html`

    """
    if (request.method == "GET"):
        # show template
        Smilie.objects.all()
        BBCode.objects.all()
        f_thread = ThreadForm()
        f_post = PostThreadForm()
    else:
        f_thread = ThreadForm(request.POST)

        f_post = PostThreadForm(request.POST)
        if f_thread.is_valid() and f_post.is_valid():
            thread = f_thread.save(commit=False)
            thread.posts = 0
            thread.author = request.user
            thread.board = Board.objects.get(pk=board_id)
            thread.save()
            post = f_post.save(commit=False)
            post.thread = thread
            post.user = request.user
            post.name = thread.name
            post.save()
            board=thread.board
            board.posts = board.posts + 1
            board.threads = board.threads+1
            board.save()
            profile = request.user.profile 
            profile.posts=profile.posts+1
            profile.save()
            return render_to_response('create_thread_success.html',{'thread':thread,},context_instance=RequestContext(request))
    return render_to_response('create_thread.html',{'f_thread':f_thread,'f_post':f_post,'board_id':board_id},context_instance=RequestContext(request))


def mod_post(request,post_id):
    mod_form = ThreadModForm(request.GET)
    if (mod_form.is_valid()):
        options= mod_form.cleaned_data['options']
        post = Post.objects.get(pk = post_id)
        user = post.user
        thread = post.thread
        if (options.lower() =='d'):
            user.posts = user.posts -1
            thread.posts  = thread.posts -1
            user.save()
            thread.save()
            post.delete()
            messages.add_message(request, messages.INFO, 'The thread was closed successfully')
            return redirect(urlresolvers.reverse('board.views.show_thread',args=[thread.id]))
            
def report(request,post_id):
    raise Http404()

@staff_member_required
def mod_thread(request,thread_id):
    """
    Display a moderation form

    **Context**

    ``RequestContext``

    ``thread``
        An instance of :model:`board.Thread`.

    """
    if (request.method == 'POST'):
        mod_form = ThreadModForm(request.POST)
    else:
        mod_form = ThreadModForm(request.GET)
    print "Is valid: "+str(mod_form.is_valid())
    if (mod_form.is_valid()):
        options= mod_form.cleaned_data['options']
        thread = Thread.objects.get(pk=thread_id)
        print options
        if (options.lower() =='c'):
            thread.closed = not thread.closed
            thread.save()
            messages.add_message(request, messages.INFO, 'The thread was closed successfully')
            return redirect(urlresolvers.reverse('board.views.show_thread',args=[thread_id]))
        elif (options.lower() =='d'):
            board = thread.board
            thread.delete()
            messages.add_message(request, messages.INFO, 'The thread was deleted successfully')
            return redirect(urlresolvers.reverse('board.views.show_board',args=[board.id]))
        elif (options.lower() =='m'):
            # show move template
            f_move = MoveThreadForm()
            return render_to_response('board/move_thread.html',{'f_move':f_move,'thread':thread},context_instance=RequestContext(request))
    raise Http404()

@staff_member_required
def move_thread(request,thread_id):
    f_move = MoveThreadForm(request.POST)
    if (f_move.is_valid()):
        thread = Thread.objects.get(pk=thread_id)
        thread.moved_from = thread.board
        thread.board = f_move.cleaned_data['board']
        thread.save()
        messages.add_message(request, messages.INFO, 'The thread was moved successfully')
        return redirect(urlresolvers.reverse('board.views.show_board',args=[thread.board.id]))
    raise Http404()


def search(request):
    if(request.method == 'GET'):
        search_type = request.GET.get('type')
        if (search_type is None):
            search_type='keys'
        if (search_type.lower() == 'keys'):
            search_string = request.GET['keywords']
            search_string.replace(' ','%')
            result = Thread.objects.filter(Q(name__contains=search_string)|Q(post__text__contains=search_string)).distinct()#.order_by('-post__time_created')
        elif(search_type.lower() == 'user'):
            try:
                user_id = int(request.GET.get('user_id'))
            except:
                raise Http404
            result = Thread.objects.filter(Q(author=user_id)|Q(post__user=user_id)).distinct()
        return render_to_response('board/search_result.html',{'results':result},context_instance=RequestContext(request))
        
        
        
