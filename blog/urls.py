from django.conf.urls import url
from feeds import AtomSiteNewsFeed,RssSiteNewsFeed
from views import *
urlpatterns = [
    url(r'^$',index,name='blog.views.index'),
    url(r'^(?P<page>\d+)/$',index,name='blog.views.index'),
    url(r'^post/(?P<entry_id>\d+)/$',blog_post,name='blog.views.blog_post'),
    url(r'^tag/(?P<tag_name>\w+)/$',tag_search,name='blog.views.tag_search'),
    url(r'^tag/(?P<tag_name>\w+)/page(?P<page>\d+)$',tag_search,name='blog.views.tag_search'),
    url(r'^rss/$',RssSiteNewsFeed(),name='blog-rss'),
    url(r'^atom/$',AtomSiteNewsFeed(),name='blog-atom'),
    
]