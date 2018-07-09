from django.conf.urls import url
from feeds import AtomSiteNewsFeed,RssSiteNewsFeed
from views import *
urlpatterns = [
    url(r'^$',index,name='blog.views.index'),
    url(r'^(?P<page>\d+)/$',index,name='blog.views.index'),
    url(r'^post/(?P<entry_id>\d+)/$',blog_post,name='blog.views.blog_post'),
    url(r'^tag/(?P<tag_name>[\w\s\W]+)/$',tag_search,name='blog.views.tag_search'),
    url(r'^tag/(?P<tag_name>[\w\s\W]+)/page(?P<page>\d+)$',tag_search,name='blog.views.tag_search'),
    url(r'^rss/$',RssSiteNewsFeed(),name='blog-rss'),
    url(r'^atom/$',AtomSiteNewsFeed(),name='blog-atom'),
    
]