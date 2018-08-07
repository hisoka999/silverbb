from django.conf.urls import  url
from cms.feeds import AtomCmsNewsFeed, RssCmsNewsFeed
from cms.views import *
urlpatterns = [
    url(r'^$',index,name='cms.views.index'),
    url(r'^news/(?P<news_id>\d+)-(?P<news_name>\S+)/$',news,name='cms.views.news'),
    url(r'^gallery/(?P<gall_id>\d+)-(?P<gall_name>\w+)/$',gallery,name='cms.views.gallery'),
    url(r'^gallery/',gallery,name='cms.views.gallery'),
    url(r'^page/(?P<page_id>\d+)-(?P<page_name>\w+)/$',page,name='cms.views.page'),
    url(r'^category/(?P<cat_id>\d+)/$',downloads,name='cms.views.downloads'),
    url(r'^category/',downloads,name='cms.views.downloads'),
    url(r'^download/(?P<download_id>\d+)/$',download_file,name='cms.views.download_file'),
    url(r'^rss/$',RssCmsNewsFeed(),name='cms-news-rss'),
    url(r'^atom/$',AtomCmsNewsFeed(),name='cms-news-atom'),
]