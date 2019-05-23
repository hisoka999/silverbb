from collections import namedtuple
from os import path
from wsgiref.util import FileWrapper

from django.core.paginator import Paginator
from django.db import connection
from django.http import Http404
from django.http import HttpResponse
# from silverbb import settings
from django.template import RequestContext

from backend.functions import render_to_response
from cms.models import NewsItem, MenuItem, Gallery, DownloadCategory, Download


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def index(request,page=1):
    news = NewsItem.objects.order_by('-time')
    news_list = Paginator(news,10)

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT DISTINCT YEAR(time) 'year',MONTHNAME(time) 'month',MONTH(time) 'month_num' FROM `cms_newsitem` ORDER BY 1 DESC,2 DESC")
        dates = namedtuplefetchall(cursor)

    return render_to_response('cms/index.html', {'news': news_list.page(page), "dates": dates},
                              context_instance=RequestContext(request))

def news(request,news_id=None,news_name=None):
    try:
        news = NewsItem.objects.get(pk=news_id)
        return render_to_response('cms/news.html',{'news':news},context_instance=RequestContext(request))
    except:
        raise Http404

def page(request,page_id,page_name):
    try:
        menu_item = MenuItem.objects.get(pk=page_id)
        page = menu_item.topic.pages.all()[0]
        return render_to_response('cms/page.html',{'page':page},context_instance=RequestContext(request))
    except Exception as e:
        print(e)
        raise Http404


def gallery(request,gall_id=None,gall_name=None):
    try:
        if gall_id is None:
            gallery = Gallery.objects.filter(show=True,parent=None).order_by('name')
            return render_to_response('cms/show_gallery.html',{'gallery':gallery},context_instance=RequestContext(request))
        else:
            gallery = Gallery.objects.get(pk = gall_id)
            return render_to_response('cms/gallery.html',{'gallery':gallery},context_instance=RequestContext(request))
    except Exception as e:
        print(e)
        raise Http404
    
def downloads(request,cat_id=None):
    try:
        if (cat_id is None):
            categories = DownloadCategory.objects.filter(visible=True,parent=None).order_by('name')
            return render_to_response('cms/dl_cats.html',{'cats':categories,},context_instance=RequestContext(request))
        else:
            category = DownloadCategory.objects.get(pk=cat_id)
            return render_to_response('cms/show_cat.html',{'category':category,},context_instance=RequestContext(request))
    except:
        raise Http404
    
def show_download(request,download_id):
    try:
        download= Download.objects.get(pk = download_id)
        return render_to_response('cms/show_dl.html',{'download':download,},context_instance=RequestContext(request))
    except:
        raise Http404
    
def download_file(request,download_id):
    try:
        download= Download.objects.get(pk = download_id)
        response = HttpResponse(FileWrapper(download.data), content_type=download.mime_type)
        print(path.basename(download.data.name))
        response['Content-Disposition'] = 'attachment; filename='+os.path.basename(download.data.name)
        return response
    except:
        raise Http404


def archive(request, year, month, page=1):
    entries = NewsItem.objects.filter(time__year=year,
                                      time__month=month).order_by('-time')
    if (page < 1):
        page = 1
    pages = Paginator(entries, 10)
    return render_to_response('cms/archive.html', {'entries': pages.page(page), 'month': month, 'year': year},
                              context_instance=RequestContext(request))
