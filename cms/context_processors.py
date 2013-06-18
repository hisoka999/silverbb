'''
Created on 21.05.2011

@author: stefan
'''
from django.conf import settings
from models import MenuItem
from django.core.urlresolvers import resolve

def menu(request):
    path = resolve(request.path)
    return {'menu': MenuItem.objects.filter(parent__isnull=True),'resolved_url':path}