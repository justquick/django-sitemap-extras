from lxml import etree

from .simple import Sitemap


class MobileSitemap(Sitemap):
    nsmap = {
        None: 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'mobile': 'http://www.google.com/schemas/sitemap-mobile/1.0'
    }

    def render_obj(self, obj):
        elem = super(MobileSitemap, self).render_obj(obj)
        etree.SubElement(elem, self.ns_format('mobile', 'mobile'), nsmap=self.nsmap)
        return elem

