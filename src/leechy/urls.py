from django.conf.urls.defaults import patterns, url
from leechy.views import (BrowserView, JsonBrowserView, HomeView,
        UpdateFilesMetadataView, UpdateSettingsView)


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="leechy_home"),
    url(r'^browse/(?P<key>[a-f0-9]{32})/(?P<path>.*)$', BrowserView.as_view(),
        name="leechy_browse"),
    url(r'^browse-json/(?P<key>[a-f0-9]{32})/(?P<path>.*)$', JsonBrowserView.as_view(),
        name="leechy_browse_json"),
    url(r'^update_file_metadata/(?P<key>[a-f0-9]{32})/$', 
        UpdateFilesMetadataView.as_view(), name="leechy_update_file_metadata"),
    url(r'^update_settings/(?P<key>[a-f0-9]{32})/$', 
        UpdateSettingsView.as_view(), name="leechy_update_settings"),
)
