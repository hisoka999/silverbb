'''
Created on 21.05.2012

@author: stefan
'''
from django.conf.urls import patterns
urlpatterns = patterns('',
    (r'^$','board.views.index'),
    (r'^board/(?P<board_id>\d+)/$','board.views.show_board'),
    (r'^board/(?P<board_id>\d+)-(?P<board_name>\w+)/$','board.views.show_board'),
    (r'^thread/(?P<thread_id>\d+)-(?P<thread_name>\w+)/$','board.views.show_thread'),
    (r'^thread/new/(?P<board_id>\d+)/$','board.views.create_thread'),
    (r'^thread/mod/(?P<thread_id>\d+)/$','board.views.mod_thread'),
    (r'^thread/move/(?P<thread_id>\d+)/$','board.views.move_thread'),
    (r'^post/new/(?P<thread_id>\d+)/$','board.views.create_post'),
    (r'^post/edit/(?P<post_id>\d+)/$','board.views.edit_post'),
    (r'^post/edit/$','board.views.edit_post'),
    (r'^post/search/$','board.views.search'),
    (r'^post/mod/(?P<post_id>\d+)/$','board.views.mod_post'),
    (r'^post/report/(?P<post_id>\d+)/$','board.views.report'),
)