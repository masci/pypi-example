# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.conf import settings
from djangopypi.decorators import basic_auth

from sendfile import sendfile

import os


def home(request):
    return render_to_response('pypi/home.html')

@basic_auth
def do_auth_get_package(request, abs_path):
    return sendfile(request, abs_path)

def do_get_package(request, abs_path):
    return sendfile(request, abs_path)

def get_package(request, path):
    abs_path = os.path.join(settings.MEDIA_ROOT, settings.DJANGOPYPI_RELEASE_UPLOAD_TO, path)
    if settings.PASSWORD_PROTECT_PYPI:
        return do_auth_get_package(request, abs_path)
    return do_get_package(request, abs_path)
