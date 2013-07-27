from math import floor
from datetime import date, datetime
from lxml import etree

try:
    from django.utils import timezone
except ImportError:
    timezone = None

from ..settings import FREQS, CONFIG
from ..utils import assert_, force_text, get_current_domain, INT_TYPES


class Formatter(object):
    def __init__(self, builder):
        self.builder = builder

    @classmethod
    def format_bool(cls, value):
        return 'yes' if value else 'no'

    @staticmethod
    def format_comma_sep(value):
        if isinstance(value, (list, tuple)):
            return ', '.join([force_text(val) for val in value])
        return value

    @staticmethod
    def format_date(value):
        if isinstance(value, datetime):
            value = value.date()
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        return value

    @classmethod
    def format_datetime(cls, value):
        if isinstance(value, datetime):
            if timezone:
                value = value.replace(tzinfo=timezone.get_current_timezone())
            return value.isoformat()
        return cls.format_date(value)

    @staticmethod
    def priority(value):
        if isinstance(value, INT_TYPES):
            value = floor(value * 10) / 10
        assert_(1. >= value >= 0., 'Priority %r invalid, must be between 0 and 1', value)
        return str(value)

    @classmethod
    def lastmod(cls, value):
        if isinstance(value, datetime):
            return cls.format_datetime(value)
        if isinstance(value, date):
            return cls.format_date(value)

    @staticmethod
    def changefreq(value):
        assert_(value in FREQS, 'Change frequency "%s" invalid, must be one of %s', value, ','.join(FREQS))
        return value


class Abstract(object):
    root_element = 'urlset'
    formatter_class = Formatter
    nsmap = {
        None: 'http://www.sitemaps.org/schemas/sitemap/0.9'
    }

    def __init__(self, view, object_list):
        self.view = view
        self.object_list = object_list
        self.domain = get_current_domain(view.request)
        self.protocol = 'https' if view.request.is_secure() else 'http'
        self.formatter = self.formatter_class(self)

    def full_url(self, absolute_url):
        return '%s://%s%s' % (self.protocol, self.domain, absolute_url)

    def _get(self, name, obj, default=None):
        try:
            attr = getattr(self.view, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def ns_format(self, tag, ns=None):
        return '{%s}%s' % (self.nsmap[ns], tag)

    def render(self):
        conf = CONFIG()
        self.root = etree.Element(self.ns_format(self.root_element), nsmap=self.nsmap)
        count = 0
        for obj in self.object_list:
            count += len(etree.tostring(self.render_obj(obj), encoding='UTF-8'))
            if count > conf['MAX_SIZE']:
                assert_(False, 'Maximum size of %s exceeded', conf['MAX_SIZE'])
                break
        return etree.tostring(self.root, pretty_print=conf['PRETTY'],
                              xml_declaration=True, encoding='UTF-8')
