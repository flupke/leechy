# -*- coding: utf-8 -*-

import os
import os.path as op
import datetime
from django.views.generic.base import View, TemplateResponseMixin
from django import http
from django.shortcuts import get_object_or_404
from leechy.models import Leecher
from leechy import settings


class HomeView(TemplateResponseMixin, View):

    template_name = "leechy/home.html"

    def get(self, request):
        return self.render_to_response({})


class BrowserView(TemplateResponseMixin, View):

    template_name = "leechy/browse.html"

    def get(self, request, key, path):
        # Get Leecher from its key and update its last_visit timestamp
        leecher = get_object_or_404(Leecher, key=key)
        if not leecher.enabled:
            raise http.Http404()
        leecher.last_visit = datetime.datetime.now()
        leecher.save() 
        # Create symlinks directory
        symlink_dir = op.join(settings.FILES_ROOT, key, path)
        if not op.isdir(symlink_dir):
            os.makedirs(symlink_dir)
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
                url = op.join(path, entry_name)
                if not url.endswith("/"):
                    url += "/"
                directories.append(url)
            else:
                files.append((
                    op.join(settings.FILES_URL, key, path, entry_name),
                    entry_name
                ))
                symlink_path = op.join(symlink_dir, entry_name)
                if not op.isfile(symlink_path):
                    os.symlink(entry_path, symlink_path)
        # Remove dead symlinks
        for entry_name in os.listdir(symlink_dir):
            entry_path = op.join(symlink_dir, entry_name)
            if not op.isdir(entry_path) and not op.exists(entry_path):
                os.unlink(entry_path)
        return self.render_to_response({
            "key": key,
            "path": path,
            "leecher": leecher,
            "directories": directories,
            "files": files,
        })
