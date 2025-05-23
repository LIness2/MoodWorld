Bienvenu sur l'application MoodWorld, vous trouverez le lien du site ici : http://localhost:8501/, pour pouvoir y accéder, vous devez installer MongoDBCompass sur votre ordinateur. Créez un compte, et créer une nouvelle database (dans + puis create database). Ensuite vous nommez la database "artciles_db", et la collection "articles". Cliquez sur votre collection, puis import. Et ajoutez ce document préablement enrengistré: 
[articles_db.articles3.json](https://github.com/user-attachments/files/20416057/articles_db.articles3.json) 
Vous pourrez lancer le site !

Nous avons essayé de lié MongoDB Atlas(en créant une URL puis en la connectant à MongoDB compass ou se trouve toute la collection d'articles filtrés), à StreamlitCloud, pour que vous puissiez acceder à notre site sans toutes ces manip et en cliquant simplement sur le lien mais sans succès... Dans GitHub, nous avons créer un "secret.toml " ou se trouve l'URL de MongoDB Atlas, afin que streamlit puisse y avoir accès, et modifié app_streamlit.py avec :
mongo_url =st.secrets["mongodb"]["uri"]

# Connexion MongoDB
client = MongoClient(mongo_url)
db = client["articles_db"]
collection = db["articles"] 
Mais ça n'a pas fonctionné. 
