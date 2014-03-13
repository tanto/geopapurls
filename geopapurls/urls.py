from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import LayersView,MapurlsView,MapurlDetailView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geopapurls.views.home', name='home'),
    # url(r'^geopapurls/', include('geopapurls.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^layers/$',LayersView.as_view()),
    url(r'^mapurls/$',MapurlsView.as_view()),
    url(r'^mapurls/(?P<pk>\d+)/(?P<action>[a-zA-Z]+)?$',MapurlDetailView.as_view())
)
