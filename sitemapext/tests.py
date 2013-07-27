from time import time
from datetime import timedelta
from contextlib import contextmanager

from django.conf import settings
from django.db import models
from django.test import TestCase
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from django.contrib.sitemaps import GenericSitemap

from .views import SitemapView, SitemapGenerator, SitemapIndex, NewsSitemapView, VideoSitemapView, ImageSitemapView


class SettingDoesNotExist:
    pass


@contextmanager
def patch_settings(**kwargs):
    old_settings = []
    for key, new_value in kwargs.items():
        old_value = getattr(settings, key, SettingDoesNotExist)
        old_settings.append((key, old_value))
        setattr(settings, key, new_value)
    yield
    for key, old_value in old_settings:
        if old_value is SettingDoesNotExist:
            delattr(settings, key)
        else:
            setattr(settings, key, old_value)


class Model(models.Model):
    name = models.TextField()
    update_date = models.DateTimeField()
    pub_date = models.DateTimeField()

    def get_absolute_url(self):
        return '/models/%s' % self.name

    @property
    def lastmod_date(self):
        return self.update_date.date()


class ModelSitemapView(SitemapView):
    model = Model
    paginate_by = 5

    def priority(self, obj):
        return 1

    def lastmod(self, obj):
        return obj.lastmod_date

    def changefreq(self, obj):
        return 'daily'


class UnlimitedModelSitemapView(ModelSitemapView):
    paginate_by = 50000


class InvalidSitemapView(ModelSitemapView):
    def priority(self, obj):
        return -100


class ModelNewsSitemapView(NewsSitemapView):
    model = Model

    def lastmod(self, obj):
        return obj.lastmod_date

    def publication(self, obj):
        return {
            'name': 'The Example Timesname',
            'language': 'en',
        }

    def access(self, obj):
        return 'Subscription'

    def genres(self, obj):
        if self.request.path == '/sitemap-invalid-news.xml':
            return ('PressRelease', 'Blog', 'FOOBAR')
        return ('PressRelease', 'Blog')

    def publication_date(self, obj):
        return obj.pub_date

    def title(self, obj):
        return obj.name

    def keywords(self, obj):
        return ('business', 'merger', 'acquisition')

    def stock_tickers(self, obj):
        return ('NASDAQ:A', 'NASDAQ:B')


class InvalidNewsSitemapView(ModelNewsSitemapView):
    def access(self, obj):
        return 'free like beer'

    def changefreq(self, obj):
        return 'when i feel like it'


class ModelVideoSitemapView(VideoSitemapView):
    model = Model

    def thumbnail_loc(self, obj):
        return 'http://www.example.com/thumbs/123.jpg'

    def title(self, obj):
        return obj.name

    def description(self, obj):
        return 'Alkis shows you how to get perfectly done steaks every time'

    def content_loc(self, obj):
        return 'http://www.example.com/video123.flv'

    def player(self, obj):
        return {
            'allow_embed': True,
            'autoplay': "ap=1",
            'loc': 'http://www.example.com/videoplayer.swf?video=123',
        }

    def duration(self, obj):
        return 600

    def expiration_date(self, obj):
        return obj.pub_date + timedelta(10)

    def rating(self, obj):
        return 4.2

    def view_count(self, obj):
        return 12345

    def publication_date(self, obj):
        return obj.pub_date

    def family_friendly(self, obj):
        return True

    def restriction(self, obj):
        return 'allow', 'IE GB US CA'

    def gallery_loc(self, obj):
        return 'http://cooking.example.com', 'Cooking Videos'

    def prices(self, obj):
        return [
            {
                'currency': 'USD',
                'value': 1.99,
                'type': 'rent',
                'resolution': 'SD'
            },
            {
                'currency': 'USD',
                'value': 10.99,
                'type': 'own',
                'resolution': 'HD'
            }
        ]

    def requires_subscription(self, obj):
        return False

    def uploader(self, obj):
        return 'GrillyMcGrillerson', 'http://www.example.com/users/grillymcgrillerson'

    def live(self, obj):
        return True


class InvalidVideoSitemapView(ModelVideoSitemapView):
    def duration(self, obj):
        return -1000

    def rating(self, obj):
        return -1000


class ModelImageSitemapView(ImageSitemapView):
    model = Model

    def images(self, obj):
        return [
            {
                'loc': 'http://www.example.com/image',
                'geo_location': 'Washington DC',
                'caption': 'Full size image',
                'license': 'http://www.example.com/license'
            }
        ]


info_dict = {
    'queryset': Model.objects.all(),
    'date_field': 'lastmod_date',
}

genericsitemaps = {
    'model': GenericSitemap(info_dict, priority=1., changefreq='daily'),
}

sitemaps = {
    'simple': ModelSitemapView,
    'unlimited': UnlimitedModelSitemapView,
    'news': ModelNewsSitemapView,
    'video': ModelVideoSitemapView,
    'image': ModelImageSitemapView,
    'invalid-simple': InvalidSitemapView,
    'invalid-news': InvalidNewsSitemapView,
    'invalid-video': InvalidVideoSitemapView,
}

urlpatterns = patterns('',
    url(r'^sitemap-index\.xml$', SitemapIndex.as_view(),
        {'sitemaps': sitemaps, 'generator': 'sitemap-generator'}),
    url(r'^sitemap-(?P<section>.+)\.xml$', SitemapGenerator.as_view(),
        {'sitemaps': sitemaps}, name='sitemap-generator'),
    (r'^django\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': genericsitemaps})

)
handler404 = 'sitemapext.utils.handler404'
handler500 = 'sitemapext.utils.handler500'


class SitemapTestCase(TestCase):
    urls = 'sitemapext.tests'
    url = '/sitemap-index.xml'
    contains = ["<?xml version='1.0' encoding='UTF-8'?>"]
    debug = False
    num = 1
    status_code = 200
    name = 'section/page.php&q=name'
    pub_date = '2010-01-01 12:00:00'
    update_date = '2013-01-01 12:00:00'

    def test_sitemap(self):
        response = self.client.get('%s%s%s' % (self.url, '&' if '?' in self.url else '?', self.__class__.__name__))
        if self.debug:
            print(response)
        self.assertEqual(response.status_code, self.status_code)
        for text in self.contains:
            count = None
            if isinstance(text, (tuple, list)):
                text, count = text
            try:
                self.assertContains(response, text, count, self.status_code)
            except AssertionError as e:
                raise AssertionError('%s\n%s' % (
                    force_text(e), force_text(response.content)))
        return response

    def setUp(self):
        for i in range(self.num):
            Model.objects.create(name=self.name, pub_date=self.pub_date, update_date=self.update_date)


class SitemapIndexTest(SitemapTestCase):
    num = 10
    contains = SitemapTestCase.contains + [
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '<loc>http://example.com/sitemap-simple.xml</loc>',
        '<loc>http://example.com/sitemap-news.xml</loc>',
    ]



class Paginated(SitemapIndexTest):
    contains = SitemapTestCase.contains + [
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ('<loc>http://example.com/models/section/page.php&amp;q=name</loc>', 5)
    ]
    url = '/sitemap-simple.xml?page=2'


class SimpleSitemapTest(SitemapTestCase):
    url = '/sitemap-simple.xml'
    contains = SitemapTestCase.contains + [
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '<loc>http://example.com/models/section/page.php&amp;q=name</loc>',
        '<priority>1.0</priority>',
        '<lastmod>2013-01-01</lastmod>',
    ]


class NewsSitemapTest(SitemapTestCase):
    url = '/sitemap-news.xml'
    contains = SitemapTestCase.contains + [
        'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"',
        'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '<lastmod>2013-01-01</lastmod>',
        '<news:news>',
            '<news:publication>',
                '<news:name>The Example Timesname</news:name>',
                '<news:language>en</news:language>',
            '</news:publication>',
            '<news:access>Subscription</news:access>',
            '<news:genres>PressRelease, Blog</news:genres>',
            '<news:publication_date>2010-01-01T12:00:00',
            '<news:title>section/page.php&amp;q=name</news:title>',
            '<news:keywords>business, merger, acquisition</news:keywords>',
            '<news:stock_tickers>NASDAQ:A, NASDAQ:B</news:stock_tickers>',
        '</news:news>',
    ]


class VideoSitemapTest(SitemapTestCase):
    url = '/sitemap-video.xml'
    contains = SitemapTestCase.contains + [
        'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"',
        'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '<video:video>',
            '<video:thumbnail_loc>http://www.example.com/thumbs/123.jpg</video:thumbnail_loc>',
            '<video:title>section/page.php&amp;q=name</video:title>',
            '<video:description>Alkis shows you how to get perfectly done steaks every time</video:description>',
            '<video:content_loc>http://www.example.com/video123.flv</video:content_loc>',
            '<video:duration>600</video:duration>',
            '<video:expiration_date>2010-01-11T12:00:00',
            '<video:rating>4.2</video:rating>',
            '<video:view_count>12345</video:view_count>',
            '<video:publication_date>2010-01-01T12:00:00',
            '<video:family_friendly>yes</video:family_friendly>',
            '<video:restriction relationship="allow">IE GB US CA</video:restriction>',
            '<video:gallery_loc title="Cooking Videos">Cooking Videos</video:gallery_loc>',
            '<video:price currency="USD" resolution="SD" type="rent">1.99</video:price>',
            '<video:price currency="USD" resolution="HD" type="own">10.99</video:price>',
            '<video:requires_subscription>no</video:requires_subscription>',
            '<video:uploader info="http://www.example.com/users/grillymcgrillerson">GrillyMcGrillerson</video:uploader>',
            '<video:live>yes</video:live>',
        '</video:video>'
    ]


class ImageSitemapTest(SitemapTestCase):
    url = '/sitemap-image.xml'
    contains = SitemapTestCase.contains + [
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"',
        'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '<image:image>',
            '<image:loc>http://www.example.com/image</image:loc>',
            '<image:caption>Full size image</image:caption>',
            '<image:geo_location>Washington DC</image:geo_location>',
            '<image:license>http://www.example.com/license</image:license>',
        '</image:image>'
    ]


class InvalidSitemapTestCase(SitemapTestCase):
    url = '/sitemap-invalid-simple.xml'
    conf = {'DEBUG': True, 'PRETTY': False}

    def test_sitemap(self):
        with patch_settings(SITEMAPS_CONFIG=self.conf):
            parent = super(InvalidSitemapTestCase, self)
            try:
                self.assertRaises(AssertionError, parent.test_sitemap)
            except:
                print parent.test_sitemap()
                raise


class InvalidNewsSitemapTestCase(InvalidSitemapTestCase):
    url = '/sitemap-invalid-news.xml'


class InvalidVideoSitemapTestCase(InvalidSitemapTestCase):
    url = '/sitemap-invalid-video.xml'


class LimitedResponseSitemapTestCase(InvalidSitemapTestCase):
    url = '/sitemap-simple.xml'
    num = 10
    contains = SimpleSitemapTest.contains + [
        ('<url>', 1)
    ]
    conf = {'MAX_SIZE': 0, 'DEBUG': True, 'PRETTY': False}


class LongURLSitemapTestCase(InvalidSitemapTestCase):
    url = '/sitemap-simple.xml'
    name = SitemapTestCase.name * 100


class MissingURLSitemapTestCase(SitemapTestCase):
    url = '/sitemaps-missing.xml'
    status_code = 404
    contains = []


if 'django.contrib.sitemaps' in settings.INSTALLED_APPS:

    class PerformanceTest(SimpleSitemapTest):
        url = '/django.xml'
        num = 1000
        contains = [
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '<loc>http://example.com/models/section/page.php&amp;q=name</loc>',
            '<priority>1.0</priority>',
            '<lastmod>2013-01-01</lastmod>',
            '<changefreq>daily</changefreq>'
        ]

        def test_performance(self):
            self.url = '/django.xml'
            ti = time()
            self.test_sitemap()
            django_time = time() - ti
            self.url = '/sitemap-unlimited.xml'
            ti = time()
            self.test_sitemap()
            ext_time = time() - ti
            decrease = ((django_time - ext_time) / django_time) * 100
            self.assert_(decrease > 50, 'Speedup over contrib.sitemaps was %.2f%%' % decrease)
