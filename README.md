import requests

# Clé API pour NewsAPI
NEWSAPI_KEY = "4aa659261bd2443997ffc38ef5c851fd"
NEWSAPI_URL = "https://newsapi.org/v2/everything"

# URL de GDELT (version 2.0)
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

# Liste des pays et langues
country_language_map = {
    "fr": "fr",
    "us": "en",
    "gb": "en",
    "de": "de",
    "es": "es",
    "it": "it",
    "ar": "ar",
}

# Paramètres NewsAPI
newsapi_params = {
    "apiKey": NEWSAPI_KEY,
    "q": "Ukraine OR Russia OR Israel OR Palestine OR Inflation OR Economy",
    "pageSize": 5,
    "sortBy": "publishedAt",
    "from": "2025-03-20",
    "to": "2025-03-25",
}

# Fonction pour récupérer les articles depuis NewsAPI
def get_newsapi_articles(country, language):
    params = newsapi_params.copy()
    params["language"] = language
    response = requests.get(NEWSAPI_URL, params=params)

    print(f"\n📰 NewsAPI - Articles pour {country} ({language})")
    if response.status_code == 200:
        data = response.json()
        if data.get("articles"):
            for article in data["articles"]:
                print(f"📌 {article['title']} ({article['source']['name']})")
                print(f"🔗 {article['url']}\n")
        else:
            print("❌ Aucun article trouvé.")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")

# Fonction pour récupérer les articles depuis GDELT
def get_gdelt_articles():
    params = {
        "query": "Ukraine OR Russia OR Israel OR Palestine OR Inflation OR Economy",
        "mode": "ArtList",
        "maxrecords": 10,  # Augmenté pour plus d'articles
        "format": "json",
        "sort": "date",  # Trier par date
    }
    response = requests.get(GDELT_URL, params=params)

    print("\n🌍 GDELT - Articles d'actualité mondiale")
    if response.status_code == 200:
        data = response.json()
        if "articles" in data:
            for article in data["articles"]:
                print(f"📌 {article.get('title', 'Sans titre')} ({article.get('source', 'Inconnu')})")
                print(f"🔗 {article.get('url', 'Pas de lien')}\n")
        else:
            print("❌ Aucun article trouvé.")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")

# Récupérer les articles pour chaque pays (NewsAPI)
for country, language in country_language_map.items():
    get_newsapi_articles(country, language)

# Récupérer les articles depuis GDELT
get_gdelt_articles()
