from pymongo import MongoClient
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
import langdetect.lang_detect_exception

# Fix pour résultats stables de langdetect
DetectorFactory.seed = 0

# Connexion à ta base MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["articles_db"]
collection = db["articles"]

# Dictionnaire de mots-clés par thème
THEMES_KEYWORDS = {
    "politique": [
        "élection", "président", "gouvernement", "loi", "parlement", "sénat", "politicien",
        "politics", "president", "government", "minister", "senate", "political", "réforme", "vote",
        "Bundestag", "ministre", "réformes"
    ],
    "Ukraine": [
        "Ukraine", "Zelensky", "Kyiv", "Kiev", "Donbass", "Crimée", "Volodymyr", "Russie", "Maidan",
        "Dnipro", "Kharkiv", "ukrainien", "war in Ukraine"
    ],
    "Guerre": [
        "guerre", "conflit", "armée", "soldats", "armes", "bombes", "militaire", "invasion", "attaque",
        "war", "military", "conflict", "missile", "tanks", "frontline", "combat", "raid", "drone"
    ],
    "culture": [
        "musique", "cinéma", "film", "théâtre", "littérature", "art", "peinture", "exposition", "spectacle",
        "culture", "book", "movie", "music", "film festival", "cultural", "opera", "concert", "sculpture"
    ],
    "économie": [
        "économie", "croissance", "PIB", "inflation", "chômage", "emploi", "revenus", "marché", "fiscalité",
        "banque", "finance", "entreprise", "bourse", "économique", "economic", "stock market", "investment",
        "bank", "recession", "GDP", "job market", "crise", "budget"
    ],
    "Israël": [
        "Israël", "Tel Aviv", "Hamas", "Gaza", "Palestine", "Netanyahu", "Jerusalem", "Tsahal", "occupation",
        "colonies", "israélien", "conflict in Gaza", "IDF", "Palestinians", "two-state solution"
    ]
}


def detect_themes(text):
    if not text:
        return ["autre"]
    text = text.lower()
    detected = set()
    for theme, keywords in THEMES_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                detected.add(theme)
                break  # Évite de compter 2 fois le même thème
    return list(detected) if detected else ["autre"]

def translate_text(text, source_lang=None, target_lang="en"):
    try:
        # Si source_lang None, auto-détection par GoogleTranslator
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Erreur traduction: {e}")
        return text  # Retourne le texte original si erreur
# Traitement de tous les articles
# Compteur d’articles traités
count = 0
for article in collection.find():
    content = article.get("content", "")
    if not content:
        continue
    try:
        lang = detect(content)
    except langdetect.lang_detect_exception.LangDetectException:
        lang = "unknown"

    translated_content = translate_text(content, source_lang=lang)
    themes = detect_themes(translated_content)
    print(f"Article ID: {article['_id']} | Langue détectée: {lang} => Thèmes: {themes}")

    collection.update_one({"_id": article["_id"]}, {"$set": {"themes": themes}})
    count += 1

print(f"\nTotal d'articles traités : {count}")
