import requests
from pymongo import MongoClient
from deep_translator import GoogleTranslator
import time

# Remplace par ta clé API NewsAPI
API_KEY = 'b4ad9741bd884013b09dc253232a152e

# Thèmes et pays ciblés
themes = ['politics', 'business', 'climate', 'conflict']
pays = ['us', 'de', 'cn', 'il', 'ps', 'in', 'ru']  # US, Allemagne, Chine, Israël, Palestine, Inde, Russie

# Connexion MongoDB locale
client = MongoClient("mongodb://localhost:27017")
db = client["articles_db"]
collection = db["articles_news"]

def get_articles(country, category):
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"country={country}&category={category}&"
        f"apiKey={API_KEY}"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            print(f"Erreur API pour {country}-{category}: {data.get('message')}")
            return []
        articles = data.get("articles", [])
        results = []
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            url = article.get("url", "")
            source_name = article.get("source", {}).get("name", "")

            # Traduction titre vers français
            try:
                title_fr = GoogleTranslator(source='auto', target='fr').translate(title) if title else ""
            except Exception as e:
                print(f"Erreur traduction titre: {e}")
                title_fr = title

            article_data = {
                "title": title,
                "title_fr": title_fr,
                "description": description,
                "url": url,
                "source": source_name,
                "theme": category,
                "country": country
            }
            results.append(article_data)
        return results
    except requests.RequestException as e:
        print(f"Erreur requête pour {country}-{category} : {e}")
        return []

def save_articles_to_db(articles):
    if articles:
        try:
            collection.insert_many(articles)
            print(f"{len(articles)} articles sauvegardés en base.")
        except Exception as e:
            print(f"Erreur insertion MongoDB : {e}")
    else:
        print("Aucun article à sauvegarder.")

if __name__ == "__main__":
    all_articles = []
    for country in pays:
        for theme in themes:
            print(f"Récupération articles pour {country} - {theme}...")
            articles = get_articles(country, theme)
            all_articles.extend(articles)
            time.sleep(1)  # Pause pour limiter la charge API

    save_articles_to_db(all_articles)

    # Affiche résumé simple
    for article in all_articles:
        print(f"{article['country']} - {article['theme']} : {article['title_fr'] or article['title']}")
