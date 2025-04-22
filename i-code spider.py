import scrapy

class MultiNewsSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['lemonde.fr', 'bbc.com', 'cnn.com', 'dw.com', 'aljazeera.com', 'elpais.com', 'nytimes.com', 'reuters.com']
    start_urls = [
        'https://www.lemonde.fr',
        'https://www.bbc.com/news',
        'https://edition.cnn.com/world',
        'https://www.dw.com/en/top-stories/s-9097',
        'https://www.aljazeera.com/news/',
        'https://english.elpais.com/',
        'https://www.nytimes.com',
        'https://www.reuters.com'
    ]

    def parse(self, response):
        # Gestion spécifique en fonction du site
        if "lemonde.fr" in response.url:
            self.parse_lemonde(response)
        elif "bbc.com" in response.url:
            self.parse_bbc(response)
        elif "cnn.com" in response.url:
            self.parse_cnn(response)
        elif "dw.com" in response.url:
            self.parse_dw(response)
        elif "aljazeera.com" in response.url:
            self.parse_aljazeera(response)
        elif "elpais.com" in response.url:
            self.parse_elpais(response)
        elif "nytimes.com" in response.url:
            self.parse_nytimes(response)
        elif "reuters.com" in response.url:
            self.parse_reuters(response)

    def parse_lemonde(self, response):
        articles = response.css('article')
        for article in articles:
            title = article.css('h2 a::text').get()
            link = article.css('h2 a::attr(href)').get()
            source = 'Le Monde'
            if title and link:
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                    'source': source,
                }

        # Pagination : récupérer les pages suivantes si disponibles
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_lemonde)

    def parse_bbc(self, response):
        articles = response.css('a.gs-c-promo-heading')
        for article in articles:
            title = article.css('h3::text').get()
            link = article.css('::attr(href)').get()
            source = 'BBC News'
            if title and link:
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                    'source': source,
                }

        # Pagination : récupérer les pages suivantes si disponibles
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_bbc)

    def parse_cnn(self, response):
        articles = response.css('h3.cd__headline')
        for article in articles:
            title = article.css('a::text').get()
            link = article.css('a::attr(href)').get()
            source = 'CNN'
            if title and link:
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                    'source': source,
                }

        # Pagination : récupérer les pages suivantes si disponibles
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_cnn)

    def parse_dw(self, response):
        articles = response.css('div.teaser__title')
        for article in articles:
            title = article.css('a::text').get()
            link = article.css('a::attr(href)').get()
            source = 'DW News'
            if title and link:
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                    'source': source,
                }

        # Pagination : récupérer les pages suivantes si disponibles
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_dw)

    # Ajoute les autres sites avec pagination similaire, si nécessaire


