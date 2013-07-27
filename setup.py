import os
from distutils.core import setup

from sitemapext import __version__


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

setup(name='django-sitemap-extras',
      version=__version__,
      description='A rethink of django.contrib.sitemaps that focuses on better performance, more flexibliity and support for a larger variety of formats.',
      long_description=read_file('README.rst'),
      author='Justin Quick',
      author_email='justquick@gmail.com',
      url='http://github.com/justquick/django-sitemap-extras',
      packages=['sitemapext', 'sitemapext.runtests', 'sitemapext.builder'],
      install_requires=read_file('requirements.txt'),
      zip_safe=False,
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Database'],
      )
