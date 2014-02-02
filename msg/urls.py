'''
Created on 10.03.2012

@author: stefan
'''
from django.conf.urls import patterns
urlpatterns = patterns('',
    # Example:
    (r'^$','msg.views.inbox'),
    (r'^show/(?P<msg_id>\d+)/$','msg.views.msg'),
    (r'^create/$','msg.views.create'),
    (r'^delete/$','msg.views.delete'),
)