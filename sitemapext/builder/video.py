from math import floor
from types import GeneratorType
from lxml import etree

from ..settings import VIDEO_ATTRS
from ..utils import INT_TYPES
from .base import Formatter, assert_
from .simple import Sitemap


class VideoFormatter(Formatter):

    @classmethod
    def live(cls, value):
        return cls.format_bool(value)

    @classmethod
    def family_friendly(cls, value):
        return cls.format_bool(value)

    @classmethod
    def requires_subscription(cls, value):
        return cls.format_bool(value)

    @classmethod
    def publication_date(cls, value):
        return cls.format_datetime(value)

    @classmethod
    def expiration_date(cls, value):
        return cls.format_datetime(value)

    def publication(self, value):
        for tag in ('name', 'language'):
            tagelem = etree.Element(self.builder.ns_format(tag, 'news'))
            tagelem.text = value[tag]
            yield tagelem

    @staticmethod
    def duration(value):
        value = int(value)
        assert_(28800 > value > 0, 'Duration %s invalid, must be less than 8hrs (28800 seconds)', value)
        return str(value)

    @staticmethod
    def rating(value):
        if isinstance(value, INT_TYPES):
            value = floor(value * 10) / 10
        assert_(5. >= value >= 0., 'Rating %s invalid, must be between 0 and 5', value)
        return str(value)

    @staticmethod
    def view_count(value):
        return str(int(value))

    def restriction(self, value):
        relationship, countries = value
        tagelem = etree.Element(self.builder.ns_format('restriction', 'video'),
                                relationship=relationship)
        tagelem.text = countries
        yield tagelem

    def gallery_loc(self, value):
        try:
            url, title = value
            attrs = {'title': title}
        except ValueError:
            url, attrs = value, {}
        tagelem = etree.Element(self.builder.ns_format('gallery_loc', 'video'), **attrs)
        tagelem.text = title
        yield tagelem

    def prices(self, value):
        for attrs in value:
            amount = attrs.pop('value')
            tagelem = etree.Element(self.builder.ns_format('price', 'video'), **attrs)
            tagelem.text = str(amount)
            yield tagelem

    def uploader(self, value):
        # TODO: domain must match site
        try:
            name, url = value
            attrs = {'info': url}
        except ValueError:
            name, attrs = value, {}
        tagelem = etree.Element(self.builder.ns_format('uploader', 'video'), **attrs)
        tagelem.text = name
        yield tagelem


class VideoSitemap(Sitemap):
    formatter_class = VideoFormatter
    nsmap = {
        None: 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'video': 'http://www.google.com/schemas/sitemap-video/1.1'
    }

    def render_obj(self, obj):
        elem = super(VideoSitemap, self).render_obj(obj)
        videoelem = etree.SubElement(elem, self.ns_format('video', 'video'), nsmap=self.nsmap)
        for attr in VIDEO_ATTRS:
            value = self._get(attr, obj)
            if value is None:
                continue
            if hasattr(self.formatter, attr):
                value = getattr(self.formatter, attr)(value)
            if isinstance(value, GeneratorType):
                for ele in value:
                    videoelem.append(ele)
                continue
            subelem = etree.SubElement(videoelem, self.ns_format(attr, 'video'))
            subelem.text = value
        return elem
