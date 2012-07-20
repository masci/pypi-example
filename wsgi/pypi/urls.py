# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from decorators import decorator_include
from decorators import basicauth_required

from django.contrib import admin
admin.autodiscover()

media_url = r'^%s%s/(?P<path>.*)$' % (
    settings.MEDIA_URL.lstrip('/'),
    settings.DJANGOPYPI_RELEASE_UPLOAD_TO
    )

if settings.PASSWORD_PROTECT_PYPI:
    pypi_urls = url(r'', decorator_include(basicauth_required, "djangopypi.urls"))
else:
    pypi_urls = url(r'', include("djangopypi.urls"))

urlpatterns = patterns('',
    url(r'^$', 'pypi.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(media_url, 'pypi.views.get_package', name='get_package'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'pypi/login.html'}, name='login'),
    url(r'^accounts/logout/$','django.contrib.auth.views.logout', {'template_name': 'pypi/logged_out.html'}),
    pypi_urls,
)
