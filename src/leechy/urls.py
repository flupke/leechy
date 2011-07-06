from django.conf.urls.defaults import patterns, include, url
from leechy.views import BrowserView, HomeView, UpdateFilesMetadataView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="leechy_home"),
    url(r'^browse/(?P<key>[a-f0-9]{32})/(?P<path>.*)$', BrowserView.as_view(),
        name="leechy_browse"),
    url(r'^update_file_metadata/(?P<key>[a-f0-9]{32})/$', 
        UpdateFilesMetadataView.as_view(), name="leechy_update_file_metadata"),
)
