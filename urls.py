from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$','cms.views.index'),                   
    (r'^forum/',include('board.urls')),
    (r'^user/', include('users.urls')),
    (r'^faq/', include('faq.urls')),
    (r'^msg/', include('msg.urls')),
    (r'^cms/', include('cms.urls')),
    (r'^blog/', include('blog.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^css/(?P<css_file1>\w+).css$','backend.views.show_css'),
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()

handler404 = 'backend.views.show404'
handler500 = 'backend.views.show404'