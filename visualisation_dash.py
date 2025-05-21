import pymongo
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from datetime import datetime

# --- Connexion MongoDB ---
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["articles_db"] 
collection = db["articles"]

from transformers import pipeline
def load_emotion_model():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

def analyze_emotions(df, emotion_analyzer):
    df = df.copy()
    if "emotion" not in df.columns:
        if "content" in df.columns:
            df["emotion"] = df["content"].apply(
                lambda text: emotion_analyzer(text[:512])[0]["label"] if text else "unknown"
            )
        else:
            df["emotion"] = "unknown"
    return df

# visualisation_dash.py

from dash import Dash
from flask import Flask

def create_dash_app(flask_app):
    # tout ton code Dash ici...
    dash_app = Dash(__name__, server=flask_app, url_base_pathname="/dash/")
    # Layout, callbacks...
    return dash_app

# --- Récupération des données ---
documents = list(collection.find({"emotion": {"$exists": True}}))
print(f"Nombre d'articles avec émotion : {len(documents)}")

# --- Nettoyage & Transformation ---
data = []
for doc in documents:
    emotion = doc.get("emotion")
    # Récupération pays ou langue
    country = doc.get("pays") or doc.get("lang") or "Inconnu"
    theme = doc.get("tags", "Autre")
    date_str = doc.get("publication_date")
    try:
        year = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").year
    except:
        year = None

    if emotion and theme:
        data.append({
            "theme": theme,
            "country": country,
            "emotion": emotion,
            "year": year,
            "count": 1
        })

df = pd.DataFrame(data)
if df.empty:
    raise ValueError("Aucune donnée à afficher. Vérifie que la base contient des émotions annotées.")

# --- Agrégation ---
df_grouped = df.groupby(["theme", "country", "emotion", "year"]).sum().reset_index()

# --- Couleurs personnalisées ---
emotion_colors = {
    "joy": "yellow",
    "sadness": "blue",
    "anger": "red",
    "fear": "purple",
    "surprise": "orange",
    "love": "pink",
    "neutral": "grey"  # ajouter si besoin
}

# --- Création de l'app Dash ---
app = Dash(__name__)
app.title = "WorldMood - Analyse des Émotions"

app.layout = html.Div([
    html.H2("Cartographie des émotions par thème et pays"),

    html.Label("Choisissez un thème :"),
    dcc.Dropdown(
        id='theme-dropdown',
        options=[{"label": theme, "value": theme} for theme in df_grouped["theme"].unique()],
        value=df_grouped["theme"].unique()[0]
    ),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='bubble-chart')
])

@app.callback(
    [Output("bar-chart", "figure"), Output("bubble-chart", "figure")],
    Input("theme-dropdown", "value")
)
def update_graphs(selected_theme):
    filtered = df_grouped[df_grouped["theme"] == selected_theme]

    fig_bar = px.bar(
        filtered,
        x="country",
        y="count",
        color="emotion",
        color_discrete_map=emotion_colors,
        title=f"Nombre d’articles par émotion dans le thème : {selected_theme}"
    )

    fig_bubble = px.scatter(
        filtered,
        x="country",
        y="year",
        size="count",
        color="emotion",
        color_discrete_map=emotion_colors,
        title=f"Évolution temporelle des émotions pour le thème : {selected_theme}"
    )

    return fig_bar, fig_bubble


if __name__ == "__main__":
    app.run_server(debug=True)
