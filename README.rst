Django Sitemap Extras
=====================


:Author:
   Justin Quick <justquick@gmail.com>
:Version: 0.1.0
:Release: 0.1.0alpha1


Django Sitemap Extras is a rethink of the builtin django.contrib.sitemaps module which focuses on better performance, more flexibliity and support for a larger variety of formats.


Features
--------

- Support for BCE dates
- Fuzzy parsing logic that can handle inputs like: ``Sun, 14 Jun 1998``, ``January 1 2000``, ``1.1.4004 BCE``, as well as any of the `normal Django input formats <https://docs.djangoproject.com/en/dev/ref/settings/#date-input-formats>`_.

Install
-------

Use pip for installation. This package requires the `lxml <http://lxml.de/>`_ library which means you will need a C compiler.
This package relies heavily on class based views so if you have Django<=1.2 installed, you will need the django-cbv package.

::

    pip install git+https://github.com/justquick/django-sitemap-extras.git#egg=django-sitemap-extras

You may add ``sitemapext`` to your ``INSTALLED_APPS`` if you wish to test it within your project, but it is not necessary otherwise.

Compatibility
^^^^^^^^^^^^^

Django Sitemap Extras has been tested with all of the following setups

:Django: 1.2, 1.3, 1.4, 1.5, 1.6
:Python: 2.6, 2.7, 3.2, 3.3, PyPy

Usage
------

Needs work, see sitemapext/runtests/ for examples.

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