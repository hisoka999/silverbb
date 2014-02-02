from models import Message
from django.shortcuts import redirect
from django.template.context import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from froms import MessageForm
from django.utils.datetime_safe import datetime
from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from django.core import urlresolvers
from backend.functions import render_to_response
from django.contrib import messages

# show the inbox
@login_required
def inbox(request):
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    messages = Message.objects.filter(reciver=request.user).order_by('-time')
    pages = Paginator(messages, 10)
    
    return render_to_response('msg/index.html',{'user_msg':pages.page(page)},context_instance=RequestContext(request))

@login_required
def create(request):
    if(request.method == "GET"):
        form = MessageForm()
        return render_to_response('msg/create.html',{'form':form},context_instance=RequestContext(request))
    else:
        form = MessageForm(request.POST)
        if(form.is_valid()):
            message= form.save(commit=False)
            message.sender = request.user
            message.time = datetime.now()
            message.save()
            messages.add_message(request, messages.INFO, 'Private message was sent to the user.')
            return redirect(urlresolvers.reverse('msg.views.index'))
        else:
            render_to_response('msg/create.html',{'form':form},context_instance=RequestContext(request))
    

@login_required
def msg(request,msg_id):
    message = Message.objects.get(pk=msg_id)
    if(not message.readed and message.reciver == request.user):
        message.readed = True
        message.save()
    if (message.reciver == request.user):
        return render_to_response('msg/show.html',{'msg':message},context_instance=RequestContext(request))
    else:
        return HttpResponseNotAllowed()

@login_required
def delete(request):
    try:
        msg_list = []
        delmsg = request.POST.get('delmsg[]')
        print type(delmsg)
        if type(delmsg) == 'unicode':
            msg_list.append(delmsg)
        else:
            for msg in delmsg:
                msg_list.append(msg)
        
        for key,msg in Message.objects.in_bulk(msg_list).items():
            if msg.reciver == request.user:
                msg.delete()
            else:
                return HttpResponseForbidden()
                
        return redirect(urlresolvers.reverse('messages.views.inbox'))
    except Exception,e:
        print 'ERROR: '+str(e)
        return HttpResponseForbidden()
