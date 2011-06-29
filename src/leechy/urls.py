from django.conf.urls.defaults import patterns, include, url
from leechy.views import BrowserView, HomeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="leechy_home"),
    url(r'^browse/(?P<key>[a-z0-9-]+)/(?P<path>.*)$', BrowserView.as_view(),
        name="leechy_browse"),
)
