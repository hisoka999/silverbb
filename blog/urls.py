from django.conf.urls import url
from django.urls import path
from blog.feeds import AtomSiteNewsFeed,RssSiteNewsFeed
from blog.views import *
urlpatterns = [
    url(r'^$',index,name='blog.views.index'),
    path('<int:page>/',index,name='blog.views.index'),
    url(r'^post/(?P<entry_id>\d+)/$',blog_post,name='blog.views.blog_post'),
    url(r'^tag/(?P<tag_name>[\w\s\W]+)/$',tag_search,name='blog.views.tag_search'),
    url(r'^tag/(?P<tag_name>[\w\s\W]+)/page(?P<page>\d+)$',tag_search,name='blog.views.tag_search'),
    url(r'^rss/$',RssSiteNewsFeed(),name='blog-rss'),
    url(r'^atom/$',AtomSiteNewsFeed(),name='blog-atom'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$',archive,name="blog_archive"),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/page(?P<page>\d+)$',archive,name="blog_archive")
    
]