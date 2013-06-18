from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$','users.views.index'),
    (r'^show/(?P<userid>\d+)/$','users.views.show'),

    (r'^show/(?P<userid>\d+)-(?P<username>\w+)/$','users.views.show'),
    (r'^login/$','users.views.login_view'),
    (r'^logout/$','users.views.logout_view'),
    (r'^register/$','users.views.register'),
    (r'^team/$','users.views.team'),
    (r'^team/(?P<team_name>\w+)/$','users.views.team'),
    (r'^profile/$','users.views.base_profile'),
    (r'^activate/(?P<uuid>\S+)/$','users.views.activate'),
)
