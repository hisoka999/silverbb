from django.conf.urls.defaults import patterns, url
from feeds import AtomSiteNewsFeed,RssSiteNewsFeed
urlpatterns = patterns('',
    (r'^$','blog.views.index'),
    (r'^(?P<page>\d+)/$','blog.views.index'),
    (r'^post/(?P<entry_id>\d+)/$','blog.views.blog_post'),
    (r'^tag/(?P<tag_name>\w+)/$','blog.views.tag_search'),
    (r'^tag/(?P<tag_name>\w+)/page(?P<page>\d+)$','blog.views.tag_search'),
    url(r'^rss/$',RssSiteNewsFeed(),name='blog-rss'),
    url(r'^atom/$',AtomSiteNewsFeed(),name='blog-atom'),
    
)