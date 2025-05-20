from final2 import annotate_articles_with_emotions, fetch_articles, save_articles_to_mongo

def update_db():
    topics = ["politique", "écologie", "technologie"]
    langs = ["fr", "en"]
    method = "gnews"

    for topic in topics:
        for lang in langs:
            articles = fetch_articles(method=method, query=topic, lang=lang, max_articles=5)
            save_articles_to_mongo(articles)

    annotate_articles_with_emotions()

if __name__ == "__main__":
    update_db()
