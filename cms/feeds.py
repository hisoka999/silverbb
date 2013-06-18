'''
Created on 31.03.2013

@author: stefan
'''
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from models import NewsItem
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import get_current_site
from django.utils.http import urlquote_plus
import urllib

class RssCmsNewsFeed(Feed):
    title = " site news"
    link = ''  #reverse('blog.views.index')
    description = "Updates on changes and additions to ."
    
    
    def items(self):
        return NewsItem.objects.order_by('-time')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:300]

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('cms.views.news', args=[item.pk,urlquote_plus(item.title)])


class AtomCmsNewsFeed(RssCmsNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssCmsNewsFeed.description