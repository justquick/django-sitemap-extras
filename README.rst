Django Sitemap Extras
=====================


:Author:
   Justin Quick <justquick@gmail.com>
:Version: 0.1.0
:Release: 0.1.0alpha1


Django Sitemap Extras is a rethink of the builtin django.contrib.sitemaps module which focuses on better performance, more flexibliity and support for a larger variety of formats.
Just like the contrib sitemaps app, Sitemap extras suports the regular `sitemaps.org protocol <http://www.sitemaps.org/protocol.html>`_ of Sitemaps and Sitemap Indexes.
In addition, the app also supports the `Google Sitemap formats <https://support.google.com/webmasters/topic/8476?hl=en>`_ including `video <https://support.google.com/webmasters/answer/80471>`_, `images <https://support.google.com/webmasters/answer/178636>`_, `mobile <https://support.google.com/webmasters/answer/34648?rd=1>`_, and `news <https://support.google.com/news/publisher/answer/75717>`_.

Install
-------

Use pip for installation. This package requires the `lxml <http://lxml.de/>`_ library which means you will need a C compiler.
This package relies heavily on class based views so if you have Django<=1.2 installed, you will need the `django-cbv <https://github.com/brutasse/django-cbv>`_ package.

::

    pip install git+https://github.com/justquick/django-sitemap-extras.git#egg=django-sitemap-extras

You may add ``sitemapext`` to your ``INSTALLED_APPS`` if you wish to test it within your project, but it is not necessary otherwise.

Compatibility
^^^^^^^^^^^^^

Django Sitemap Extras has been tested with all of the following setups

:Django: 1.2, 1.3, 1.4, 1.5, 1.6
:Python: 2.6, 2.7, 3.2, 3.3, PyPy

Basic Usage
-----------

All Sitemaps are based on class based views so you can override the model/queryset/get_queryset attributes in order to generate the items to represent in a Sitemap.
Querysets are paginated by 50,000 items by default to match the Sitemap protocol specs but you can override any pagination settings just like any other `ListView <https://docs.djangoproject.com/en/dev/ref/class-based-views/generic-display/#listview>`_ class.
Just like the contrib sitemaps app, you can specify the sitemap specific attributes (eg lastmod, changefreq) on the Sitemap subclass using functions that take an object and return the Sitemap information.
For the following usage examples we will use the simple model below as an example

.. code-block:: python

    class MyModel(models.Model):
        name = models.TextField()
        update_date = models.DateTimeField()
        pub_date = models.DateTimeField()
        is_mobile = models.BooleanField(default=False)

Simple Sitemaps
^^^^^^^^^^^^^^^

.. code-block:: python

    from sitemapext import SitemapView

    class MySitemapView(SitemapView):
        model = MyModel

        def priority(self, obj):
            return .5  # Float from 0.0 to 1.0

        def lastmod(self, obj):
            return obj.update_date.date()  # Date or datetime instance

        def changefreq(self, obj):
            return 'daily'  # One of the change frequencies from the Sitemap spec

Initialization
^^^^^^^^^^^^^^

To activate sitemap generation on your Django site, add these lines to your URLconf:

.. code-block:: python

    from sitemapext import SitemapIndex, SitemapGenerator

    sitemaps = {
        'simple': ModelSitemapView,
    }

    urlpatterns = patterns('',
        url(r'^sitemap-index\.xml$', SitemapIndex.as_view(),
            {'sitemaps': sitemaps, 'generator': 'sitemap-generator'}),
        url(r'^sitemap-(?P<section>.+)\.xml$', SitemapGenerator.as_view(),
            {'sitemaps': sitemaps}, name='sitemap-generator'),
    )

The SitemapIndex view takes a 'generator' kwarg which is the name of the URL for the SitemapGenerator view.
The SitemapGenerator view takes a 'section' kwarg which corresponds to the section key of the sitemaps dictionary.


Google Sitemaps
---------------

The rest of the Google defined Sitemaps extend the basic SitemapView so they can also support the same overrides as well as defining some extra attributes.
To initialize them, just add them to the sitemaps dictionary above for use in the SitemapIndex/SitemapGenerator views.

News Sitemaps
^^^^^^^^^^^^^^^

.. code-block:: python

    from sitemapext import NewsSitemapView

    class MyNewsSitemapView(NewsSitemapView):
        model = MyModel

        def publication(self, obj):
            return {
                'name': 'The Example Timesname',
                'language': 'en',
            }

        def access(self, obj):
            return 'Subscription'

        def genres(self, obj):
            return ('PressRelease', 'Blog')

        def publication_date(self, obj):
            return obj.pub_date

        def title(self, obj):
            return obj.name

        def keywords(self, obj):
            return ('business', 'merger', 'acquisition')

        def stock_tickers(self, obj):
            return ('NASDAQ:A', 'NASDAQ:B')



Image Sitemaps
^^^^^^^^^^^^^^^

.. code-block:: python

    from sitemapext import ImageSitemapView

    class ModelImageSitemapView(ImageSitemapView):
        model = MyModel

        def images(self, obj):
            # Returns a list of dictionaries of images that pertain to a particular MyModel instance.
            return [
                {
                    'loc': 'http://www.example.com/image.jpg',
                    'geo_location': 'Washington DC',
                    'caption': 'Full size image',
                    'license': 'http://www.example.com/license'
                }
            ]


Video Sitemaps
^^^^^^^^^^^^^^^

.. code-block:: python

    from sitemapext import VideoSitemapView

    class MyVideoSitemapView(VideoSitemapView):
        model = MyModel

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
            return datetime(2014, 1, 1)

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
                }
            ]

        def requires_subscription(self, obj):
            return False

        def uploader(self, obj):
            return 'GrillyMcGrillerson', 'http://www.example.com/users/grillymcgrillerson'

        def live(self, obj):
            return True


Mobile Sitemaps
^^^^^^^^^^^^^^^

Mobile Sitemaps are just like the regular Sitemaps except they can contain **only** URLs that serve mobile web content.


.. code-block:: python

    from sitemapext import MobileSitemapView

    class MyMobileSitemapView(MobileSitemapView):
        queryset = MyModel.objects.filter(is_mobile=True)


Testing
-------

The best way to test this package in all circumstances is using `Tox <http://tox.readthedocs.org/en/latest/>`_. Clone the project and run::

    $ tox

This will take a long time to download and compile all the packages required.
If you are testing database integration, make sure you have a database named "test" setup for MySQL and PostgreSQL.

You can just run the unittests at any point on the standard sqlite3 setup by running::

    $ python sitemapext/runtests/runtests.py

If you are using sitemapext in your project, you can test it like any other Django app::

    $ django-admin.py test sitemapext