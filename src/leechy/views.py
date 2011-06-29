# -*- coding: utf-8 -*-

from django.views.generic.base import View, TemplateResponseMixin
from django.contrib import messages
from django.utils.translation import ugettext as _
from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404


class HomeView(TemplateResponseMixin, View):

    template_name = "leechy/home.html"

    def get(self, request):
        return self.render_to_response({})


class BrowserView(TemplateResponseMixin, View):

    template_name = "leechy/browser.html"

    def get(self, request, key, path):
        return self.render_to_response({
            "key": key,
            "path": path,
        })
