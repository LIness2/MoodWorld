import scrapy
from deep_translator import GoogleTranslator
from pymongo import MongoClient

class ReutersSpider(scrapy.Spider):
    name = "reuters"
    allowed_domains = ["reuters.com"]
    start_urls = [
        "https://www.reuters.com/world/us/",
        "https://www.reuters.com/world/china/",
        "https://www.reuters.com/world/europe/germany/",
        "https://www.reuters.com/business/environment/",
        "https://www.reuters.com/business/economy/",
        "https://www.reuters.com/world/conflict/"
    ]

    def parse(self, response):
        articles = response.css('article.story')
        for article in articles:
            title = article.css('h3::text').get() or article.css('h2::text').get()
            link = article.css('a::attr(href)').get()
            if link and not link.startswith("http"):
                link = response.urljoin(link)

            translated_title = self.translate(title)

            article_data = {
                'theme': self.detect_theme(response.url),
                'country': self.detect_country(response.url),
                'title': translated_title,
                'link': link,
                'source': 'Reuters'
            }

            # Enregistrement dans MongoDB
            self.save_article(article_data)

            yield article_data

    def detect_theme(self, url):
        if "climate" in url or "environment" in url:
            return "Climat"
        elif "economy" in url or "business" in url:
            return "Économie"
        elif "conflict" in url or "war" in url:
            return "Guerre"
        elif "politics" in url:
            return "Politique"
        else:
            return "Autre"

    def detect_country(self, url):
        if "/us/" in url:
            return "États-Unis"
        elif "/china/" in url:
            return "Chine"
        elif "/germany/" in url:
            return "Allemagne"
        else:
            return "Autre"

    def translate(self, text):
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except:
            return text

    def save_article(self, article):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["articles_db"]
        collection = db["articles_news"]
        collection.insert_one(article)
