'''
Created on 20.06.2013

@author: stefan
'''
from django import template
from board.models import Board,Thread

register = template.Library()

def is_new_thread(value, arg):
    thread  = Thread.objects.get(pk=value)
    return thread.is_new(arg)
    
def is_new_board(value,arg):
    board = Board.objects.get(pk=value)
    return board.is_new(arg)
    
is_new_thread.is_safe = False
is_new_board.is_save  = False


register.filter('is_new_board', is_new_board)
register.filter('is_new_thread', is_new_thread)