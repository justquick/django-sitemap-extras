from django.conf import settings


FREQS = ('always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never')
OPTIONAL_ATTRS = ('priority', 'changefreq', 'lastmod')
NEWS_ATTRS = ('publication', 'access', 'genres', 'publication_date', 'title',
              'geo_locations', 'keywords', 'stock_tickers')
VIDEO_ATTRS = ('thumbnail_loc', 'title', 'description', 'content_loc', 'player_loc',
               'duration', 'expiration_date', 'rating', 'view_count', 'publication_date',
               'family_friendly', 'restriction', 'gallery_loc', 'prices', 'requires_subscription',
               'uploader', 'live')
IMG_ATTRS = ('loc', 'caption', 'geo_location', 'title', 'license')
ACCESSES = ('subscription', 'registration')
GENRES = (
    'PressRelease',  # (visible) an official press release.
    'Satire',  # (visible): an article which ridicules its subject for didactic purposes.
    'Blog',  # (visible): any article published on a blog, or in a blog format.
    'OpEd',  # an opinion-based article which comes specifically from the Op-Ed section of your site.
    'Opinion',  # any other opinion-based article not appearing on an Op-Ed page, i.e., reviews, interviews, etc.
    'UserGenerated',  # newsworthy user-generated content which has already gone through a formal editorial review process on your site.
)

def CONFIG():
    defaults = {
        'DEBUG': settings.DEBUG,
        'MAX_SIZE':  (10 * 1024 * 1024) - 5120,  # 10MB limit with 500K safety room
        'PRETTY': True,
    }
    defaults.update(getattr(settings, 'SITEMAPS_CONFIG', {}))
    return defaults