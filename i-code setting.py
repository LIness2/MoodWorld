BOT_NAME = 'test_scrapy'

SPIDER_MODULES = ['test_scrapy.spiders']
NEWSPIDER_MODULE = 'test_scrapy.spiders'

ROBOTSTXT_OBEY = False  # Ignorer les restrictions robots.txt

DOWNLOAD_DELAY = 2  # Un peu de délai pour éviter les blocages

USER_AGENT = "WorldMoodBot (+http://worldmood.local)"
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

