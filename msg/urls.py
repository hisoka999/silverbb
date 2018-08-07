'''
Created on 10.03.2012

@author: stefan
'''
from django.conf.urls import url
from msg.views import inbox,msg,create,delete
urlpatterns = [
    # Example:
    url(r'^$',inbox,name='msg.views.inbox'),
    url(r'^show/(?P<msg_id>\d+)/$',msg,name='msg.views.msg'),
    url(r'^create/$',create,name='msg.views.create'),
    url(r'^delete/$',delete,name='msg.views.delete'),
]