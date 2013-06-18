from models import User,Rank
from forms import ProfileForm,RegisterForm,UserEditForm
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import login,logout, forms
from django.contrib.auth.models import Group
from silverbb.backend.functions import render_to_response
from silverbb import settings
from django.core.mail import send_mail
from models import UserProfile,UserSession
from django.http import Http404
from silverbb.backend.models import Theme
from django.db import transaction
from django.contrib import messages
from django.core import urlresolvers

'''
def handle_uploaded_file(f):
    destination = open(settings.STATICFILES_DIRS[0]+'/avatars/'+f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
'''
def show(request,userid,username=""):
    user = User.objects.get(pk=userid)
    profile = user.get_profile()
    return render_to_response('user/show.html',{'user':user,'profile':profile},context_instance=RequestContext(request))


def index(request):
    if (request.is_ajax()):
        if (not request.GET.get('column')):
            column = '-userprofile__posts'
        else:
            column = request.GET.get('column')
        users = User.objects.all().order_by(column)
        return render_to_response('user/all_ajax.html',{'users':users,},context_instance=RequestContext(request))
    else:
        users = User.objects.all().order_by('-userprofile__posts')
        return render_to_response('user/all.html',{'users':users,},context_instance=RequestContext(request))


@transaction.commit_on_success
def register(request):
    if (request.method=='POST'):
        form = RegisterForm(data=request.POST)
        f_profile = ProfileForm(data=request.POST)
        if(form.is_valid() and f_profile.is_valid()):
            user = form.save()
            user.groups.add(Group.objects.get(name='User'))
            user.is_active = False
            user.set_password(user.password)
            user.save()
            import uuid
            lv_uuid = str(uuid.uuid1())[0:30]
            send_mail('Registration at silver-boards.de', 'Hello '+user.username+
                      '\n\nPlease click the following the link to end your registration.\n\n'+
                      'http://localhost:8000/user/activate/'+lv_uuid+'/', settings.SYSTEMMAIL,
                    [user.email], fail_silently=False)
            profile = f_profile.save(commit=False)
            profile.user = user
            profile.posts = 0
            profile.threads = 0
            profile.activate = lv_uuid
            profile.theme = Theme.objects.get(default=True)
            profile.banned = False
            profile.save()            
            return render_to_response('user/register_successful.html',{},context_instance=RequestContext(request))
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
        print e
        raise Http404

def login_view(request):
    #username = request.POST['username']
    #password = request.POST['password']
    #user = authenticate(username=username, password=password)
    request.session.set_test_cookie()
    form = forms.AuthenticationForm(request,data=request.POST)
    if form.is_valid():
        user = form.get_user()
        UserSession.objects.get(session_key = request.session.session_key).delete()
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
        return redirect(urlresolvers.reverse('board.views.index'))
        #return render_to_response('user/login_successful.html',{'referer':referer},context_instance=RequestContext(request))
    return render_to_response('user/login_error.html',{'form':form},context_instance=RequestContext(request))

def logout_view(request):
    user_id = request.user.id
    logout(request)
    if user_id is not None:
        print "uid"+str(user_id)
        UserSession.objects.filter(user=user_id).delete()
    messages.add_message(request, messages.INFO, 'Logout successfull!')
    return redirect('board.views.index')

def team(request):
    groups=Group.objects.filter(user__is_staff=True)
    return render_to_response('user/team.html',{'groups':groups},context_instance=RequestContext(request))

def base_profile(request):
    f_password = forms.PasswordChangeForm(request.POST)
    f_profile = ProfileForm(instance = request.user.get_profile())
    f_user = UserEditForm(instance = request.user)
    commit = False
    if request.method == 'POST':
        f_profile = ProfileForm(request.POST,request.FILES,instance = request.user.get_profile())
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
