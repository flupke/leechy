# -*- coding: utf-8 -*-
import os
import os.path as op
import datetime
import itertools

from django.utils import simplejson as json
from django.views.generic.base import View, TemplateResponseMixin
from django import http
from django.shortcuts import get_object_or_404, redirect

from leechy import settings, cache
from leechy.models import Leecher, ShoutboxMessage
from leechy.files import Entry, Directory, File
from leechy.forms import ShoutboxMessageForm
from leechy.utils import force_utf8


class HomeView(TemplateResponseMixin, View):
    """
    Dummy home view.
    """

    template_name = "leechy/home.html"

    def get(self, request):
        return self.render_to_response({})


class LeecherViewMixin(object):
    """
    Mixin class for leechers views.
    """

    def get_leecher(self, key):
        # Get Leecher from its key and update its last_visit timestamp
        leecher = get_object_or_404(Leecher, key=key)
        if not leecher.enabled:
            raise http.Http404()
        leecher.last_visit = datetime.datetime.now()
        leecher.save() 
        return leecher


class BrowserViewMixin(object):
    """
    Mixin class for browser views.
    """

    def listdir(self, key, path, metadata):
        key = force_utf8(key)
        path = force_utf8(path)
        if metadata is None:
            metadata = {}
        # Create root symlink
        symlink_dir = op.join(settings.FILES_ROOT, key)
        if not op.isdir(symlink_dir):
            os.symlink(settings.FILES_SOURCE, symlink_dir)
        # Get files and directories
        source_dir = op.join(settings.FILES_SOURCE, path)
        if not op.isdir(source_dir):
            raise http.Http404()
        entries = []
        directories_data, files_data = cache.listdir(source_dir)
        for entry_name, size, timestamp in directories_data:
            full_path = op.join(source_dir, entry_name)
            rel_path = op.join(path, entry_name)
            entry_metadata = metadata.get(rel_path, {})
            entries.append(Directory(entry_name, full_path, rel_path,
                size, timestamp, entry_metadata))
        for entry_name, size, timestamp in files_data:
            full_path = op.join(source_dir, entry_name)
            rel_path = op.join(path, entry_name)
            entry_metadata = metadata.get(rel_path, {})
            entries.append(File(entry_name, full_path, rel_path, size,
                timestamp, entry_metadata, 
                op.join(settings.FILES_URL, key, path, entry_name)))
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries


class BrowserView(TemplateResponseMixin, LeecherViewMixin, BrowserViewMixin,
        View):
    """
    Html version of the browser.
    """

    template_name = "leechy/browse.html"

    def context(self, key, path, leecher, shoutbox_form):
        entries = self.listdir(key, path, leecher.files_metadata)
        # Split the path of the current page
        split_path = []
        rel = ""
        for comp in reversed(path.split("/")):
            if not comp:
                continue
            split_path.insert(0, (rel, comp))
            rel += "../"
        return {
            "key": key,
            "path": path,
            "split_path": split_path,
            "leecher": leecher,
            "entries": entries,
            "settings": leecher.settings,
            "tags_cloud": Entry.tags_cloud(entries),
            "shoutbox_messages": ShoutboxMessage.objects.last_messages(),
            "shoutbox_form": shoutbox_form,
        }

    def get(self, request, key, path):
        leecher = self.get_leecher(key)
        shoutbox_form = ShoutboxMessageForm()
        return self.render_to_response(self.context(key, path, leecher,
            shoutbox_form))

    def post(self, request, key, path):
        leecher = self.get_leecher(key)
        shoutbox_form = ShoutboxMessageForm(request.POST)
        if shoutbox_form.is_valid():
            message = shoutbox_form.save(commit=False)
            message.author = leecher.name
            message.save()
            return redirect('leechy_browse', key=key, path=path)
        return self.render_to_response(self.context(key, path, leecher,
            shoutbox_form))


class JsonBrowserView(LeecherViewMixin, BrowserViewMixin, View):
    """
    JSON version of the browser.
    """

    def get(self, request, key, path):
        leecher = self.get_leecher(key)
        entries = self.listdir(key, path, leecher.files_metadata)
        return http.HttpResponse(json.dumps({
            "entries": [e.as_dict() for e in entries], 
        }))


class UpdateFilesMetadataView(LeecherViewMixin, View):        
    """
    Ajax callback view used to update a single metadata attribute of a file.
    """

    def get(self, request, key):
        leecher = self.get_leecher(key)
        attr = request.GET["attr"]
        value = request.GET["value"]
        path = request.GET["path"]
        if attr in Leecher.bool_metadata_attrs:
            value = True if value == "true" else False
        if leecher.files_metadata is None:
            leecher.files_metadata = {}
        if path not in leecher.files_metadata:
            leecher.files_metadata[path] = {}
        leecher.files_metadata[path][attr] = value
        leecher.save()
        return http.HttpResponse()


class UpdateSettingsView(LeecherViewMixin, View):
    """
    Ajax callback view used to update a single setting of the current leecher.
    """

    def get(self, request, key):
        leecher = self.get_leecher(key)
        attr = request.GET["attr"]
        value = request.GET["value"]
        if attr in Leecher.bool_settings_attrs:
            value = True if value == "true" else False
        if leecher.settings is None:
            leecher.settings = {}
        leecher.settings[attr] = value
        leecher.save()
        return http.HttpResponse()
