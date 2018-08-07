'''
Created on 21.05.2012

@author: stefan
'''
from django.conf.urls import url
from board.views import *
urlpatterns = [
    url(r'^$',index,name='board.views.index'),
    url(r'^board/(?P<board_id>\d+)/$',show_board,name='board.views.show_board'),
    url(r'^board/(?P<board_id>\d+)-(?P<board_name>\w+)/$',show_board,name='board.views.show_board'),
    url(r'^thread/(?P<thread_id>\d+)-(?P<thread_name>\w+)/$',show_thread,name='board.views.show_thread'),
    url(r'^thread/(?P<thread_id>\d+)/$',show_thread,name='board.views.show_thread'),
    url(r'^thread/new/(?P<board_id>\d+)/$',create_thread,name='board.views.create_thread'),
    url(r'^thread/mod/(?P<thread_id>\d+)/$',mod_thread,name='board.views.mod_thread'),
    url(r'^thread/move/(?P<thread_id>\d+)/$',move_thread,name='board.views.move_thread'),
    url(r'^post/new/(?P<thread_id>\d+)/$',create_post,name='board.views.create_post'),
    url(r'^post/edit/(?P<post_id>\d+)/$',edit_post,name='board.views.edit_post'),
    url(r'^post/edit/$',edit_post,name='board.views.edit_post'),
    url(r'^post/search/$',search,name='board.views.search'),
    url(r'^post/mod/(?P<post_id>\d+)/$',mod_post,name='board.views.mod_post'),
    url(r'^post/report/(?P<post_id>\d+)/$',report,name='board.views.report'),
]