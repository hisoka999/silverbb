'''
Created on 21.05.2011

@author: stefan
'''
from django.conf import settings
from cms.models import MenuItem
from django.urls import resolve
from backend.functions import memoize

@memoize
def menu(request):
    path = resolve(request.path)
    return {'menu': MenuItem.objects.prefetch_related('menuitem_set').filter(parent__isnull=True),'resolved_url':path}