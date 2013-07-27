from types import GeneratorType

from lxml import etree

from .base import Formatter, assert_
from .simple import Sitemap
from ..settings import ACCESSES, GENRES, NEWS_ATTRS


class NewsFormatter(Formatter):

    @staticmethod
    def access(value):
        assert_(value.lower() in ACCESSES, 'Access level %s invalid, must be one of %s', value, ','.join(ACCESSES))
        return value.title()

    @classmethod
    def publication_date(cls, value):
        return cls.format_datetime(value)

    @classmethod
    def genres(cls, value):
        for val in value:
            assert_(val in GENRES, 'Genre %s invalid, must be one of %s', val, ','.join(GENRES))
        return cls.format_comma_sep(value)

    @classmethod
    def keywords(cls, value):
        return cls.format_comma_sep(value)

    @classmethod
    def stock_tickers(cls, value):
        return cls.format_comma_sep(value)

    def publication(self, value):
        for tag in ('name', 'language'):
            tagelem = etree.Element(self.builder.ns_format(tag, 'news'))
            tagelem.text = value[tag]
            yield tagelem


class NewsSitemap(Sitemap):
    formatter_class = NewsFormatter
    nsmap = {
        None: 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'news': 'http://www.google.com/schemas/sitemap-news/0.9'
    }

    def render_obj(self, obj):
        elem = super(NewsSitemap, self).render_obj(obj)
        newselem = etree.SubElement(elem, self.ns_format('news', 'news'), nsmap=self.nsmap)
        for attr in NEWS_ATTRS:
            value = self._get(attr, obj)
            if value is None:
                continue
            subelem = etree.SubElement(newselem, self.ns_format(attr, 'news'))
            if hasattr(self.formatter, attr):
                value = getattr(self.formatter, attr)(value)
            if isinstance(value, GeneratorType):
                for ele in value:
                    subelem.append(ele)
            else:
                subelem.text = value
        return elem
