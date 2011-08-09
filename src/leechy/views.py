# -*- coding: utf-8 -*-
import os
import re
import urllib
import os.path as op
import datetime
from django.views.generic.base import View, TemplateResponseMixin
from django import http
from django.shortcuts import get_object_or_404
from leechy import settings
from leechy.models import Leecher


class HomeView(TemplateResponseMixin, View):

    template_name = "leechy/home.html"

    def get(self, request):
        return self.render_to_response({})


class LeecherViewMixin(object):

    def get_leecher(self, key):
        # Get Leecher from its key and update its last_visit timestamp
        leecher = get_object_or_404(Leecher, key=key)
        if not leecher.enabled:
            raise http.Http404()
        leecher.last_visit = datetime.datetime.now()
        leecher.save() 
        return leecher


class BrowserView(TemplateResponseMixin, LeecherViewMixin, View):

    template_name = "leechy/browse.html"
    google_split_pattern = re.compile(r"[\s.-]")

    def get(self, request, key, path):
        leecher = self.get_leecher(key)
        # Create root symlink
        symlink_dir = op.join(settings.FILES_ROOT, key)
        if not op.isdir(symlink_dir):
            os.symlink(settings.FILES_SOURCE, symlink_dir)
        # Get files and directories
        source_dir = op.join(settings.FILES_SOURCE, path)
        if not op.isdir(source_dir):
            raise http.Http404()
        directories = []
        files = []
        for entry_name in sorted(os.listdir(source_dir), 
                key=lambda e: e.lower()):
            if settings.EXCLUDE_FILES.match(entry_name):
                continue
            entry_path = op.join(source_dir, entry_name)
            if op.isdir(entry_path):
                rel_path = entry_name + "/"
                full_path = op.join(path, rel_path)
                google_url = self.google_url(entry_name)
                directories.append((
                    rel_path, 
                    full_path,
                    google_url,
                ))
            else:
                google_url = self.google_url(op.splitext(entry_name)[0])
                files.append((
                    op.join(settings.FILES_URL, key, path, entry_name),
                    op.join(path, entry_name),
                    entry_name,
                    op.getsize(entry_path),
                    google_url,
                ))
        # Flatten files metadata to make it useable in the template
        checked_paths = set()
        if leecher.files_metadata:
            for name, metadata in leecher.files_metadata.items():
                if metadata.get("checked", False):
                    checked_paths.add(name)
        return self.render_to_response({
            "key": key,
            "path": path,
            "leecher": leecher,
            "directories": directories,
            "files": files,
            "checked_paths": checked_paths,
            "settings": leecher.settings,
        })

    def google_url(self, name):
        """
        Given *name*, build a Google search URL.
        """
        words = self.google_split_pattern.split(name.encode("utf8"))
        return "http://www.google.com/search?%s" % urllib.urlencode(
                {"q": " ".join(words)})


class UpdateFilesMetadataView(LeecherViewMixin, View):        

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
