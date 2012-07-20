# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.utils.importlib import import_module
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

import base64


class DecoratedPatterns(object):
    """
    A wrapper for an urlconf that applies a decorator to all its views.
    """
    def __init__(self, urlconf_name, decorators):
        self.urlconf_name = urlconf_name
        try:
            iter(decorators)
        except TypeError:
            decorators = [decorators]
        self.decorators = decorators
        if not isinstance(urlconf_name, basestring):
            self._urlconf_module = self.urlconf_name
        else:
            self._urlconf_module = None

    def decorate_pattern(self, pattern):
        if isinstance(pattern, RegexURLResolver):
            regex = pattern.regex.pattern
            urlconf_module = pattern.urlconf_name
            default_kwargs = pattern.default_kwargs
            namespace = pattern.namespace
            app_name = pattern.app_name
            urlconf = DecoratedPatterns(urlconf_module, self.decorators)
            decorated = RegexURLResolver(
                regex, urlconf, default_kwargs,
                app_name, namespace
            )
        else:
            callback = pattern.callback
            for decorator in reversed(self.decorators):
                callback = decorator(callback)
            decorated = RegexURLPattern(
                pattern.regex.pattern,
                callback,
                pattern.default_args,
                pattern.name
            )
        return decorated

    def _get_urlconf_module(self):
        if self._urlconf_module is None:
            self._urlconf_module = import_module(self.urlconf_name)
        return self._urlconf_module
    urlconf_module = property(_get_urlconf_module)

    def _get_urlpatterns(self):
        try:
            patterns = self.urlconf_module.urlpatterns
        except AttributeError:
            patterns = self.urlconf_module
        return [self.decorate_pattern(pattern) for pattern in patterns]
    urlpatterns = property(_get_urlpatterns)

    def __getattr__(self, name):
        return getattr(self.urlconf_module, name)


def decorator_include(decorators, arg, namespace=None, app_name=None):
    """
    Works like ``django.conf.urls.defaults.include`` but takes a view decorator
    or an iterable of view decorators as the first argument and applies them,
    in reverse order, to all views in the included urlconf.
    """
    if isinstance(arg, tuple):
        if namespace:
            raise ImproperlyConfigured(
                'Cannot override the namespace for a dynamic module that provides a namespace'
            )
        urlconf, app_name, namespace = arg
    else:
        urlconf = arg
    decorated_urlconf = DecoratedPatterns(urlconf, decorators)
    return (decorated_urlconf, app_name, namespace)


def user_passes_test(test_func, realm):
    """
    Decorator for views that checks that the user passes the given test,
    asking for HTTP basic auth  if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.

    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            # They are not logged in. See if they provided login credentials
            #
            if 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth) == 2:
                    # NOTE: We are only support basic authentication for now.
                    #
                    if auth[0].lower() == "basic":
                        uname, passwd = base64.b64decode(auth[1]).split(':')
                        user = authenticate(username=uname, password=passwd)
                        if user is not None and user.is_active:
                            login(request, user)
                            request.user = user
                            return view_func(request, *args, **kwargs)

            # Either they did not provide an authorization header or
            # something in the authorization attempt failed. Send a 401
            # back to them to ask them to authenticate.
            #
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
            return response
        return _wrapped_view
    return decorator


def basicauth_required(function=None, realm = ""):
    """
    Decorator for views that checks that the user is logged in, asking for
    basic HTTP credentials if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        realm=realm
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

