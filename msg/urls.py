'''
Created on 10.03.2012

@author: stefan
'''
from django.conf.urls import url
from views import inbox,msg,create,delete
urlpatterns = [
    # Example:
    url(r'^$',inbox),
    url(r'^show/(?P<msg_id>\d+)/$',msg),
    url(r'^create/$',create),
    url(r'^delete/$',delete),
]