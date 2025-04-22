import requests

NEWSAPI_URL = "https://newsapi.org/v2/everything"
NEWSAPI_KEY = "9b3e8b1adf7e4f21a69ee8c2749c3037"
newsapi_params = {
    "q": "Ukraine OR Russia OR Israel OR Palestine OR Inflation OR Economy",
    "sortBy": "publishedAt",
    "apiKey": NEWSAPI_KEY,
    "pageSize": 20  # Minimum 20 articles par page
}

# Récupérer les articles depuis NewsAPI en paginant
def get_newsapi_articles(country, language):
    params = newsapi_params.copy()
    params["language"] = language
    max_pages = 5  # Nombre maximal de pages à récupérer (pour un total de 100 articles)
    total_articles = 0

    print(f"\n📰 NewsAPI - Articles pour {country} ({language})")

    for page in range(1, max_pages + 1):
        params["page"] = page
        response = requests.get(NEWSAPI_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            if not articles:
                break

            for article in articles:
                print(f"📌 {article['title']} ({article['source']['name']})")
                print(f"🔗 {article['url']}\n")
                total_articles += 1
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            break

    if total_articles == 0:
        print("❌ Aucun article trouvé.")

# Exécuter la fonction pour récupérer les articles
def main():
    get_newsapi_articles("France", "fr")
    get_newsapi_articles("USA", "en")
    get_newsapi_articles("Allemagne", "de")

if __name__ == "__main__":
    main()


