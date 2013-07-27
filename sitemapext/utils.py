import logging
from socket import getfqdn, gethostbyname, error

from django.http import HttpResponseNotFound, HttpResponseServerError
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from django.contrib.sites.models import Site

from .settings import CONFIG

try:
    INT_TYPES = (int, long, float)
except NameError:
    INT_TYPES = (int, float)

logger = logging.getLogger('sitemapext')


def assert_(stmt, msg, *args):
    """
    Asserts that some statement is True.
    If AssertionError is raised and SITEMAPS_DEBUG is True, error message is raised with arguments.
    If AssertionError is raised and SITEMAPS_DEBUG is False, error message is logged to 'sitemapext' logger with WARN level.
    """
    msg = force_text(msg)
    try:
        assert stmt
    except AssertionError:
        if CONFIG()['DEBUG']:
            raise AssertionError(msg % args)
        else:
            logger.warning(msg, *args)


def get_current_domain(request):
    """
    Checks if contrib.sites is installed and returns either the current
    domain name or the domain name based on the request.
    """
    if Site._meta.installed:
        return Site.objects.get_current().domain
    return request.get_host()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')


def is_googlebot(ip):
    try:
        return gethostbyname(getfqdn(ip)) == ip
    except error:
        return False


def handler500(request):
    return HttpResponseServerError()


def handler404(request):
    return HttpResponseNotFound()
