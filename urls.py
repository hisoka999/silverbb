from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

import board,users,faq,msg,cms,blog,backend
import cms.views,backend.views
admin.autodiscover()

urlpatterns = [
    url(r'^$',cms.views.index),                   
    url(r'^forum/',include('board.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^faq/', include('faq.urls')),
    url(r'^msg/', include('msg.urls')),
    url(r'^cms/', include('cms.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^css/(?P<css_file1>\w+).css$',backend.views.show_css),
    url(r'^captcha/$',backend.views.captcha),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()

handler404 = 'backend.views.show404'
handler500 = 'backend.views.show404'