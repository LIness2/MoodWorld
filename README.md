Bienvenu sur l'application MoodWorld, vous trouverez le lien du site ici : http://localhost:8501/, pour pouvoir y accéder, vous devez installer MongoDBCompass sur votre ordinateur. Créez un compte, et créez une nouvelle database (dans + puis create database). Ensuite vous nommez la database "artciles_db", et la collection "articles". Cliquez sur votre collection, puis import. Et ajoutez ce document préablement enrengistré: 
[articles_db.articles3.json](https://github.com/user-attachments/files/20416057/articles_db.articles3.json) 
Vous pourrez lancer le site !

Pour run l'application avec comme fichier principal:app_streamlit.py et modules: code_final.py, executez avec streamlit run app_streamlit.py


Nous avons essayé de lié MongoDB Atlas(en créant une URL puis en la connectant à MongoDB compass où se trouve toute la collection d'articles filtrés), à StreamlitCloud, pour que vous puissiez acceder à notre site sans toutes ces manip et en cliquant simplement sur le lien mais sans succès... Dans GitHub, nous avons créer un "secret.toml " où se trouve l'URL de MongoDB Atlas(et nous nous sommes pourtant assurées que toutes les IP avaient accès au cluster), afin que streamlit puisse y avoir accès, et modifié app_streamlit.py avec :
mongo_url =st.secrets["mongodb"]["uri"]

# Connexion MongoDB
client = MongoClient(mongo_url)
db = client["articles_db"]
collection = db["articles"] 
Mais ça n'a pas fonctionné. 
