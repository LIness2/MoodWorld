import requests

API_KEY = "4aa659261bd2443997ffc38ef5c851fd"
URL = "https://newsapi.org/v2/top-headlines"

params = {
    "apiKey": API_KEY,
    "language": "fr",  # Articles en français
    "country": "fr",  # Articles de France
    "pageSize": 100,  # Augmenter le nombre d'articles
    "page": 1  # Commencer à la page 1
}

# Envoi de la requête à l'API
response = requests.get(URL, params=params)

# Affichage de la réponse pour débogage
print(response.text)  # Affiche la réponse brute de l'API

# Vérification de la réponse
if response.status_code == 200:
    data = response.json()

    if "articles" in data and data["articles"]:
        for article in data["articles"]:
            print(f"📌 Titre : {article['title']}")
            print(f"📰 Source : {article['source']['name']}")
            print(f"🔗 URL : {article['url']}\n")
    else:
        print("❌ Aucun article trouvé ou problème dans la réponse.")
else:
    print(f"❌ Erreur {response.status_code}: {response.text}")
