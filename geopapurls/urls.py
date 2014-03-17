from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import LayersView,MapurlsView,MapurlDetailView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'geopapurls.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^layers/$',login_required(LayersView.as_view()),name='layers-list'),
    url(r'^mapurls/$',login_required(MapurlsView.as_view())),
    url(r'^mapurls/(?P<pk>\d+)/(?P<action>[a-zA-Z]+)?$',login_required(MapurlDetailView.as_view())),
    url(r'^login/$', 'django.contrib.auth.views.login',name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': settings.LOGOUT_NEXT_PAGE},name='logout')
)
