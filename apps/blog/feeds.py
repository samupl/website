from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from .models import Post


class LatestEntriesFeed(Feed):
    title = _('SAMU.PL latest blog entries')
    link = 'blog:home'
    description = _('Latest blog entries on SAMU.PL website blog')

    def items(self):
        return Post.objects.order_by('-date')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.title