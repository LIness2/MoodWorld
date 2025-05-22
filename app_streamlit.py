import streamlit as st
import pandas as pd
from final2 import get_cleaned_articles, load_emotion_model, analyze_emotions, bubble_map

def main():
    st.title("Carte des émotions")

    # Charger les articles depuis MongoDB
    articles = get_cleaned_articles()
    if not articles:
        st.warning("Aucun article disponible dans la base.")
        return

    df = pd.DataFrame(articles)

    # Vérifier et préparer les colonnes nécessaires
    if "timestamp" in df.columns and "year" not in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["year"] = df["timestamp"].dt.year.fillna(0).astype(int)

    if "theme" not in df.columns:
        df["theme"] = "Inconnu"

    if "emotion" not in df.columns or df["emotion"].isnull().all():
        emotion_model = load_emotion_model()
        df = analyze_emotions(df, emotion_model)

    # Sidebar : sélection du thème
    selected_theme = st.sidebar.selectbox("Choisir un thème", options=df["theme"].unique())
    selected_emotion = st.sidebar.selectbox("Choisir une émotion", options=df["emotion"].dropna().unique())

    # Gestion robuste du slider d'année
    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    st.write(f"Années disponibles : {min_year} → {max_year}")

    if min_year == max_year:
        selected_year = min_year
        st.info(f"Les articles sont uniquement de l'année {selected_year}.")
    else:
        selected_year = st.sidebar.slider("Choisir l'année", min_year, max_year, min_year)

    # Générer la carte à bulles
    try:
        fig = bubble_map(df, selected_theme, selected_emotion, selected_year)

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur lors de l'affichage de la carte : {e}")

if __name__ == "__main__":
    main()
