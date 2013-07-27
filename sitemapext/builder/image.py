from lxml import etree

from ..settings import IMG_ATTRS
from ..utils import assert_
from .base import Formatter
from .simple import Sitemap


class ImageFormatter(Formatter):

    def images(self, value):
        count = 0
        for img in value:
            tagelem = etree.Element(self.builder.ns_format('image', 'image'))
            for attr in IMG_ATTRS:
                if attr in img and not img[attr] is None:
                    # TODO warn if domains mismatch
                    imgtag = etree.SubElement(tagelem, self.builder.ns_format(attr, 'image'))
                    imgtag.text = img[attr]
            yield tagelem
            count += 1
            if count == 1000:
                assert_(False, 'Maximum number of images (1000) reached on a single page')
                break


class ImageSitemap(Sitemap):
    formatter_class = ImageFormatter
    nsmap = {
        None: 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'image': 'http://www.google.com/schemas/sitemap-image/1.1'
    }

    def render_obj(self, obj):
        elem = super(ImageSitemap, self).render_obj(obj)
        value = self._get('images', obj)
        if not value is None:
            for ele in getattr(self.formatter, 'images')(value):
                elem.append(ele)
        return elem

