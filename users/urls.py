from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$',index,name='users.views.index'),
    url(r'^show/(?P<userid>\d+)/$',show,name='users.views.show'),

    url(r'^show/(?P<userid>\d+)-(?P<username>\w+)/$',show,name='users.views.show'),
    url(r'^login/$',login_view,name='users.views.login_view'),
    url(r'^logout/$',logout_view,name='users.views.logout_view'),
    url(r'^register/$',register,name='users.views.register'),
    url(r'^team/$',team,name='users.views.team'),
    url(r'^team/(?P<team_name>\w+)/$',team,name='users.views.team'),
    url(r'^profile/$',base_profile,name='users.views.base_profile'),
    url(r'^activate/(?P<uuid>\S+)/$',activate,name='users.views.activate'),
]
