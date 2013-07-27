from lxml import etree

from .base import Abstract, assert_
from ..settings import OPTIONAL_ATTRS


class Sitemap(Abstract):

    def render_obj(self, obj):
        location = self.full_url(self._get('location', obj))
        assert_(len(location) < 2048, 'URL "%s" invalid, must be shorter than 2048 characters', location)
        elem = etree.SubElement(self.root, 'url')
        loc = etree.SubElement(elem, 'loc')
        loc.text = location
        for attr in OPTIONAL_ATTRS:
            value = self._get(attr, obj)
            if value is None:
                continue
            if hasattr(self.formatter, attr):
                value = getattr(self.formatter, attr)(value)
            subelem = etree.SubElement(elem, attr)
            subelem.text = value
        return elem

