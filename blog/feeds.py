'''
Created on 31.03.2013

@author: stefan
'''
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from models import Entry
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import get_current_site

class RssSiteNewsFeed(Feed):
    title = " blog news"
    link = ''  #reverse('blog.views.index')
    description = "Updates on changes and additions to chicagocrime.org."

    def items(self):
        return Entry.objects.order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def get_feed(self, obj, request):
        self.title = get_current_site(request).name+self.title
        return super(RssSiteNewsFeed,self).get_feed(obj,request)

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('blog.views.blog_post', args=[item.pk])


class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssSiteNewsFeed.description