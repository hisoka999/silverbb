from django.conf.urls.defaults import patterns, url
from cms.feeds import AtomCmsNewsFeed, RssCmsNewsFeed
urlpatterns = patterns('',
    (r'^$','cms.views.index'),
    (r'^news/(?P<news_id>\d+)-(?P<news_name>\S+)/$','cms.views.news'),
    (r'^gallery/(?P<gall_id>\d+)-(?P<gall_name>\w+)/$','cms.views.gallery'),
    (r'^gallery/','cms.views.gallery'),
    (r'^page/(?P<page_id>\d+)-(?P<page_name>\w+)/$','cms.views.page'),
    (r'^category/(?P<cat_id>\d+)/$','cms.views.downloads'),
    (r'^category/','cms.views.downloads'),
    (r'^download/(?P<download_id>\d+)/$','cms.views.download_file'),
    url(r'^rss/$',RssCmsNewsFeed(),name='cms-news-rss'),
    url(r'^atom/$',AtomCmsNewsFeed(),name='cms-news-atom'),
)