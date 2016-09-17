'''
Created on 31.12.2011

@author: stefan
'''
from models import UserSession
from datetime import date
from django.utils.datetime_safe import datetime
from datetime import timedelta
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

class UserMiddleware:
    
    def process_request(self, request):
        user = None
        if request.path.startswith('/css') or request.path.startswith('/fav'):
            return
        #request.session.set_test_cookie()
        if request.user.id>0:
            user = request.user.id
        try:
            sess=UserSession.objects.get(user__id=user)
            sess.session_key=request.session.session_key
            sess.time = datetime.now()
            sess.save()
        except:
            if request.session.session_key is None or len(request.session.session_key) >40:
                session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
                s = SessionStore(session_key)
                s['last_login'] = datetime.isoformat(datetime.now())
                s.save()
                request.COOKIES['last_login'] =  s['last_login'] 
            else:
                s = request.session
            sess,created=UserSession.objects.get_or_create(user_id=user,session_key=s.session_key,board_id=None,thread_id=None)
            sess.time = datetime.now()
            sess.session_key=s.session_key
            sess.save()
            request.session = s

        d = timedelta(seconds=3600)
        deldate = datetime.now()-d
        UserSession.objects.filter(time__lt=deldate).delete()
        # delete all sessions that are not in the sessiontable
        UserSession.objects.raw('DELETE from users_usersession WHERE session_key not in (SELECT d.session_key FROM django_session d)')
