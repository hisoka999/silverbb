'''
Created on 11.02.2012

@author: stefan
'''
from django.conf.urls import url
from faq.views import *
urlpatterns = [
    # Example:
    url(r'^$',index,name='faq.views.index'),
    url(r'^(?P<topic_id>\d+)/$',topic,name='faq.views.topic'),
]