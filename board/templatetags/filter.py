'''
Created on 20.06.2013

@author: stefan
'''
from django import template
from board.models import Board,Thread

register = template.Library()

def is_new_thread(value, arg):
    print "value = %s"%(value)
    print "arg   = %s"%(arg)
    thread  = Thread.objects.get(pk=value)
    print "thread id: "+str(thread.id)
    if (thread.is_new(arg)):
        return True
    else:
        return False
is_new_thread.is_safe = False



register.filter('is_new_thread', is_new_thread)