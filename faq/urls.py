'''
Created on 11.02.2012

@author: stefan
'''
from django.conf.urls import patterns
urlpatterns = patterns('',
    # Example:
    (r'^$','faq.views.index'),
    (r'^(?P<topic_id>\d+)/$','faq.views.topic'),
)