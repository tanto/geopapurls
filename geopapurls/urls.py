from django.shortcuts import redirect
from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import LayersView,MapurlsView,MapurlDetailView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'geopapurls.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^layers/$',LayersView.as_view(),name='layers-list'),
    url(r'^mapurls/$',MapurlsView.as_view()),
    url(r'^mapurls/(?P<pk>\d+)/(?P<action>[a-zA-Z]+)?$',MapurlDetailView.as_view())
)
