from lxml import etree

from .base import Abstract, assert_


class Index(Abstract):
    root_element = 'sitemapindex'

    def render_obj(self, obj):
        assert_(len(obj) < 2048, 'Sitemap URL "%s" invalid, must be shorter than 2048 characters', obj)
        elem = etree.SubElement(self.root, 'sitemap')
        loc = etree.SubElement(elem, 'loc')
        loc.text = self.full_url(obj)
        return elem
