# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.conf import settings
from sendfile import sendfile
import os

def home(request):
    return render_to_response('pypi/home.html')

def get_package(request, path):
    abs_path = os.path.join(settings.MEDIA_ROOT, settings.DJANGOPYPI_RELEASE_UPLOAD_TO, path)
    return sendfile(request, abs_path)
