# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

media_url = r'^%s%s/(?P<path>.*)$' % (
    settings.MEDIA_URL.lstrip('/'),
    settings.DJANGOPYPI_RELEASE_UPLOAD_TO
    )

urlpatterns = patterns('',
    url(r'^$', 'pypi.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(media_url, 'pypi.views.get_package', name='get_package'),
    url(r'', include("djangopypi.urls"))
)
