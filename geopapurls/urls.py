from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from views import LayersView,MapurlsView,MapurlsHtmlView,MapurlDetailView,SuggestView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'geopapurls.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^layers/$',login_required(LayersView.as_view()),name='layers-list'),
    url(r'^layers/$',LayersView.as_view(),name='layers-list'),
    url(r'^mapurls/$',MapurlsView.as_view()),
    url(r'^mapurlshtml/$',MapurlsHtmlView.as_view()),
    url(r'^mapurls/(?P<pk>\d+)/(?P<action>[a-zA-Z]+)?$',MapurlDetailView.as_view()),
    url(r'^thanks$',TemplateView.as_view(template_name='geopapurls/thanks.html'),name='thanks'),
    url(r'^suggest$',SuggestView.as_view(),name='suggest'),
    url(r'^login/$', 'django.contrib.auth.views.login',name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': settings.LOGOUT_NEXT_PAGE},name='logout')
)
