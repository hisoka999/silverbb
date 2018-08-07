from users.models import User,Rank
from users.forms import ProfileForm,RegisterForm,UserEditForm
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import login,logout, forms
from django.contrib.auth.models import Group
from backend.functions import render_to_response
from django.conf import settings
from django.core.mail import send_mail
from users.models import UserProfile,UserSession
from django.http import Http404
from backend.models import Theme
from django.db import transaction
from django.contrib import messages
from django.urls import reverse
import datetime
from board.models import Post
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
'''
def handle_uploaded_file(f):
    destination = open(settings.STATICFILES_DIRS[0]+'/avatars/'+f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
'''
def show(request,userid,username=""):
    try:
        showuser = User.objects.get(pk=userid)
        profile = showuser.profile
        posts = float(Post.objects.count())
        posts_from_total = 0
        if(posts > 0):
            posts_from_total = float(profile.posts)/posts*100.0
        return render_to_response('user/show.html',{'showuser':showuser,'profile':profile,'posts_from_total':posts_from_total},context_instance=RequestContext(request))
    except ObjectDoesNotExist as e:
        raise Http404("User does not exist")


def index(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    if (request.is_ajax()):
        users = User.objects.values('pk','username','profile__posts','profile__threads','last_login').all()
        return JsonResponse(list(users),safe=False)
    else:
        users = User.objects.all().order_by('-profile__posts')
        user_list = Paginator(users, 10)
        user_page = user_list.page(page)
        return render_to_response('user/all.html',{'users':user_page,},context_instance=RequestContext(request))


@transaction.atomic
def register(request):
    if (request.method=='POST'):
        form = RegisterForm(data=request.POST)
        f_profile = ProfileForm(data=request.POST)
        if(form.is_valid() and f_profile.is_valid()):
            referer = request.META.get('HTTP_REFERER')
            user = form.save()
            user.groups.add(Group.objects.get(name='User'))
            user.is_active = False
            user.set_password(user.password)
            user.save()
            import uuid
            lv_uuid = str(uuid.uuid1())[0:30]
            
            message = """<html>
            <body>
                <h3>Registration at """+get_current_site(request).name+"""</h3><br/>
                <p>
                    Please click the following link to end your registration.
                </p>
                <p>
                    <a href='https://"""+get_current_site(request).domain+""""/user/activate/"""+lv_uuid+"""/'>Activation Link</a>
                </p>
            </html>
            """
            
            send_mail('Registration at '+get_current_site(request).name, 'Hello '+user.username+
                      '\n\nPlease click the following the link to end your registration.\n\n'+
                      'Activation Link: https://'+get_current_site(request).domain+'/user/activate/'+lv_uuid+'/', settings.SYSTEMMAIL,
                    [user.email], fail_silently=False,html_message=message)
            profile = f_profile.save(commit=False)
            profile.user = user
            profile.posts = 0
            profile.threads = 0
            profile.activate = lv_uuid
            profile.theme = Theme.objects.get(default=True)
            profile.banned = False
            profile.save()            
            messages.add_message(request, messages.INFO, 'User successful registrated.')
            #return redirect(urlresolvers.reverse('board.views.index'))
            return redirect(referer)
    else:
        form = RegisterForm()
        f_profile = ProfileForm()
    return render_to_response('user/register.html',{'form':form,'f_profile':f_profile},context_instance=RequestContext(request))        

def activate(request,uuid):
    try:
        
        profile = UserProfile.objects.get(activate =uuid)
        user = profile.user
        profile.activate = 'T'
        user.is_active = True
        profile.save()
        user.save()
        return render_to_response('user/activated.html',{},context_instance=RequestContext(request))
    except Exception as e:
        print(e)
        raise Http404

def login_view(request):
    #username = request.POST['username']
    #password = request.POST['password']
    #user = authenticate(username=username, password=password)
    if (request.method=='POST'):
        request.session.set_test_cookie()
        form = forms.AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            sessions = UserSession.objects.filter(session_key = request.session.session_key)
            if sessions is not None:
                sessions.delete()
            
            login(request, user)
            referer = request.META.get('HTTP_REFERER')
            ## create empty profile if missing
            try:
                profile = UserProfile.objects.get(user=request.user)
            except:
                if (user.is_staff):
                    user.groups.add(Group.objects.get(name='Administrator'))
                    profile = UserProfile() 
                    profile.user = request.user              
                    profile.posts = 0
                    profile.threads = 0
                    profile.activate = 'T'
                    profile.banned = False
                    profile.theme  = Theme.objects.filter(default=True)[0]
                    profile.save()
                    user.save()
            messages.add_message(request, messages.INFO, 'Login successfull!')
            #return redirect(urlresolvers.reverse('board.views.index'))
            return redirect(referer)
            #return render_to_response('user/login_successful.html',{'referer':referer},context_instance=RequestContext(request))
        return render_to_response('user/login_error.html',{'form':form},context_instance=RequestContext(request))
    else:
        form = forms.AuthenticationForm(request)
        return render_to_response('user/login.html', {'form':form}, context_instance= RequestContext(request))

def logout_view(request):
    user_id = request.user.id
    logout(request)
    if user_id is not None:
        print("uid"+str(user_id))
        UserSession.objects.filter(user=user_id).delete()
    messages.add_message(request, messages.INFO, 'Logout successfull!')
    return redirect('board.views.index')

def team(request,team_name=None):
    if (request.method == 'POST'):
        team_name = request.POST['team_name']
    if (team_name is None):
        groups=Group.objects.filter(user__is_staff=True)
    else:
        groups=Group.objects.filter(user__is_staff=True,name=team_name)
    return render_to_response('user/team.html',{'groups':groups},context_instance=RequestContext(request))

def team_json(request,team_name):
    groups=Group.objects.filter(user__is_staff=True,name=team_name)
    users = User.objects.values('pk','username','profile__posts','profile__threads','last_login').filter(is_staff=True,groups__name=team_name)
    return JsonResponse(list(users),safe=False)
    #return HttpResponse(serialize('json', users))


@login_required(login_url='/user/login/')
def base_profile(request):
    f_password = forms.PasswordChangeForm(request.POST)
    f_profile = ProfileForm(instance = request.user.profile)
    f_user = UserEditForm(instance = request.user)
    commit = False
    if request.method == 'POST':
        f_profile = ProfileForm(request.POST,request.FILES,instance = request.user.profile)
        f_user = UserEditForm(request.POST,request.FILES,instance = request.user)
        if f_password.is_valid():
            f_password.save(commit=True)
            #handle_uploaded_file(request.FILES['avatar'])
            f_profile.save(commit=True)
            commit=True
        if f_profile.is_valid():
            f_profile.save(commit=True)
            #handle_uploaded_file(request.FILES['avatar'])
            commit=True
        if f_user.is_valid():
            user = f_user.save(commit=True)
            commit=True
    return render_to_response('user/profile.html',{'profile':f_profile,'f_pw':f_password,'f_user':f_user,'commit':commit},context_instance=RequestContext(request))
