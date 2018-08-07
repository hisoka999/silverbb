
from django.test import TestCase,Client
from backend.models import Theme
from users.models import User,UserProfile,Rank
from django.contrib.auth.models import Group
import logging
import sys
from contextlib import contextmanager
from django.conf import settings

@contextmanager
def streamhandler_to_console(lggr):
    # Use 'up to date' value of sys.stdout for StreamHandler,
    # as set by test runner.
    stream_handler = logging.StreamHandler(sys.stdout)
    lggr.addHandler(stream_handler)
    yield
    lggr.removeHandler(stream_handler)

def testcase_log_console(lggr):
    def testcase_decorator(func):
        def testcase_log_console(*args, **kwargs):
            with streamhandler_to_console(lggr):
                return func(*args, **kwargs)
        return testcase_log_console
    return testcase_decorator

logger = logging.getLogger('django_test')

class UserTest(TestCase):
    fixtures = ['initial_data.json',]

    def setUp(self):
        settings.DEBUG = True
    
    def test_profile_page_no_login(self):
        c = Client()
        response = c.get('/user/profile/')
        self.failIf(response.status_code != 302)
    
    def test_all_users(self):
        c = Client()
        response = c.get('/user/')
        self.assertEqual(response.status_code,200)
    
    def test_team(self):
        c = Client()
        response = c.get('/user/team/')
        self.assertEqual(response.status_code,200)
    @testcase_log_console(logger)
    def test_show_invalid(self):
        c = Client()
        response = c.get('/user/show/11/')
        self.assertEqual(response.status_code,404)
        
     
    def test_show_valid(self):
        user = User.objects.create(username="test",is_active=True,password="test",email="test@test.de",is_staff=False)
        user.groups.add(Group.objects.get(name='User'))
        profile = UserProfile()
        profile.user = user
        profile.posts = 0
        profile.threads = 0
        profile.activate = "FALSE"
        profile.theme = Theme.objects.get(default=True)
        profile.banned = False
        profile.save()
        
        
        c = Client()
        response = c.get('/user/show/'+str(user.pk)+'/')
        self.assertEqual(response.status_code,200)
        
    def test_rank(self):
        user = User.objects.create(username="test",is_active=True,password="test",email="test@test.de",is_staff=False)
        user.groups.add(Group.objects.get(name='User'))
        profile = UserProfile()
        profile.user = user
        profile.posts = 0
        profile.threads = 0
        profile.activate = "FALSE"
        profile.theme = Theme.objects.get(default=True)
        profile.banned = False
        profile.save()
        
        rank = profile.get_rank()
        self.failIf(profile.posts < rank.posts)
        
        

