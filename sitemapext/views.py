from random import randint

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.utils.cache import patch_response_headers
from django.views.decorators.cache import cache_page, never_cache
try:
    from django.views.generic import ListView, View
except ImportError:
    try:
        from cbv import ListView, View
    except ImportError:
        raise ImportError('You must have either Django>=1.3 or django-cbv>=0.2 installed.')

from .builder import Sitemap, Index, NewsSitemap, VideoSitemap, ImageSitemap, MobileSitemap
from .utils import get_client_ip, is_googlebot


class CacheMixin(object):
    cache_timeout = None
    cache = None
    key_prefix = None

    def get_cache_timeout(self):
        return self.cache_timeout

    def get_cache(self):
        return self.cache

    def get_key_prefix(self):
        return self.key_prefix

    def dispatch(self, *args, **kwargs):
        timeout = self.get_cache_timeout()
        if timeout is None:
            return super(CacheMixin, self).dispatch(*args, **kwargs)
        if isinstance(timeout, (list, tuple)):
            timeout = randint(*timeout)
        response = cache_page(timeout, cache=self.get_cache(), key_prefix=self.get_key_prefix()
                              )(super(CacheMixin, self).dispatch)(*args, **kwargs)
        patch_response_headers(response, timeout)
        return response


class GoogleBotVerifierMixin(object):
    override_password = 'changeme'

    def dispatch(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        if ip in settings.INTERNAL_IPS or is_googlebot(ip) or request.GET.get('password') == self.override_password:
            return never_cache(super(GoogleBotVerifierMixin, self).dispatch)(request, *args, **kwargs)
        return HttpResponseForbidden()


class SitemapView(CacheMixin, ListView):
    http_method_names = ['get']
    builder_class = Sitemap
    paginate_by = 50000

    def get(self, request, *args, **kwargs):
        super(SitemapView, self).get(request, *args, **kwargs)
        context = self.get_context_data(object_list=self.object_list)
        self.builder = self.builder_class(self, context['object_list'])
        return HttpResponse(self.builder.render(), content_type='application/xml')

    def location(self, obj):
        return obj.get_absolute_url()


class NewsSitemapView(SitemapView):
    builder_class = NewsSitemap


class VideoSitemapView(SitemapView):
    builder_class = VideoSitemap


class ImageSitemapView(SitemapView):
    builder_class = ImageSitemap


class MobileSitemapView(SitemapView):
    builder_class = MobileSitemap


class SitemapIndex(CacheMixin, View):
    http_method_names = ['get']
    builder_class = Index

    def get(self, request, *args, **kwargs):
        def generate():
            for section, view in kwargs['sitemaps'].items():
                view = view()
                url = reverse(kwargs['generator'], kwargs={'section': section})
                yield url
                paginator = view.get_paginator(view.get_queryset(), view.paginate_by)
                for page in range(2, paginator.num_pages + 1):
                    yield '%s?page=%s' % (url, page)
        self.builder = self.builder_class(self, generate())
        return HttpResponse(self.builder.render(), content_type='application/xml')


class SitemapGenerator(CacheMixin, View):
    http_method_names = ['get']

    def dispatch(self, request, *args, **kwargs):
        if not kwargs['section'] in kwargs['sitemaps']:
            raise Http404("No sitemap available for section: %r" % kwargs['section'])
        return kwargs['sitemaps'][kwargs['section']].as_view()(request, *args, **kwargs)
