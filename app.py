from flask import Flask, render_template
from code_final import annotate_articles_with_emotions, save_articles_to_mongo, plot_emotions
from pymongo import MongoClient

# Création de l'app Flask
app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["articles_db"]
collection = db["articles"]

# Import et création de l'app Dash intégrée
from visualisation_dash import create_dash_app
dash_app = create_dash_app(app)

@app.route("/")
def index():
    topics = ["politique", "écologie", "technologie"]
    langs = ["fr", "en"]
    method = "gnews"

    all_articles = []

    for topic in topics:
        for lang in langs:
            try:
                articles = fetch_articles(method=method, query=topic, lang=lang, max_articles=5)
                if articles:
                    save_articles_to_mongo(articles)
                    all_articles.extend(articles)
                else:
                    print(f"⚠️ Aucun article trouvé pour '{topic}' en langue '{lang}'")
            except Exception as e:
                print(f"❌ Erreur lors de la récupération des articles pour {topic}/{lang} : {e}")

    if all_articles:
        try:
            annotate_articles_with_emotions()
            plot_emotions()
        except Exception as e:
            print(f"❌ Erreur pendant l'analyse ou l'affichage des émotions : {e}")
    else:
        print("⚠️ Aucun article à traiter. Pas d'analyse ou de visualisation.")

    try:
        articles = list(collection.find({"emotion": {"$exists": True}}).sort("publication_date", -1).limit(20))
    except Exception as e:
        print(f"❌ Erreur lors de la lecture depuis MongoDB : {e}")
        articles = []

    return render_template("index.html", articles=articles)

@app.route("/stats")
def stats():
    pipeline = [
        {"$match": {"emotion": {"$exists": True}}},
        {"$group": {"_id": "$emotion", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    try:
        results = list(collection.aggregate(pipeline))
        labels = [r["_id"] for r in results]
        values = [r["count"] for r in results]
    except Exception as e:
        print(f"❌ Erreur dans la génération des stats : {e}")
        labels = []
        values = []

    return render_template("stats.html", labels=labels, values=values)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

