# 📊 **MarketSense**

**MarketSense** est mon projet qui simule le rôle de **Data Engineer** avec une spécialisation en **Intelligence Artificielle appliquée à la finance**. Son objectif est de développer un **dashboard d'aide à la décision** pour les investisseurs **intraday** et **long terme**.

🧱 Le projet repose sur :
- Des **pipelines ETL** robustes et automatisés.
- Le **stockage des données** dans **BigQuery** et **Cloud Storage (GCP)**.
- L’utilisation d’un **modèle GRU** pour la prédiction des prix des marchés financiers.
- Une **visualisation interactive** avec **Streamlit**.

Le code suit les principes de la **programmation orientée objet** avec des **classes Python** pour assurer la modularité et la maintenabilité.

---

## 🗂️ **Architecture du projet**

```plaintext
├── Documentation.ipynb
├── GCP_key.json
├── Google Cloud console.html
├── Graph
│   ├── __pycache__
│   │   └── graph.cpython-310.pyc
│   └── graph.py
├── IA_research.ipynb
├── Model
│   ├── GRU_Agent.keras
│   ├── GruAgent.py
│   └── __pycache__
│       └── GruAgent.cpython-310.pyc
├── Pipeline
│   ├── core
│   │   ├── __pycache__
│   │   │   └── main_pipeline.cpython-310.pyc
│   │   └── main_pipeline.py
│   ├── market_data
│   │   ├── PipeMarketData.py
│   │   └── __pycache__
│   │       └── PipeMarketData.cpython-310.pyc
│   ├── news_data
│   │   ├── PipeNewsData.py
│   │   └── __pycache__
│   │       └── PipeNewsData.cpython-310.pyc
│   ├── sentiment_data
│   │   ├── PipeSentimentData.py
│   │   └── __pycache__
│   │       └── PipeSentimentData.cpython-310.pyc
│   ├── storage
│   │   ├── StorageData.py
│   │   └── __pycache__
│   │       └── StorageData.cpython-310.pyc
│   └── wallet_data
│       ├── PipeWalletData.py
│       └── __pycache__
│           └── PipeWalletData.cpython-310.pyc
├── README.md
├── __pycache__
│   ├── GruAgent.cpython-310.pyc
│   └── graph.cpython-310.pyc
└── main.py
```

-----
## 🔄 **Pipelines**

Les pipelines suivent les **bonnes pratiques d'entreprise**, assurant modularité, scalabilité et maintenance. Ils sont conçus pour l’extraction, la transformation et le stockage des données dans un environnement de production.

- **Extraction → Transformation → Stockage**
- Les données sont **uniformisées** (horaires européens).
- Les bases **BigQuery** sont **rafraîchies régulièrement** pour garantir la mise à jour continue des données.

---

## 📈 **Données des marchés financiers – `market_data`**

- **Source** : **Yahoo Finance** via l'API `yfinance`.
- Données horaires des marchés américains : Prix d’ouverture, de clôture, haut et bas de l’heure précédente.
- **Features ajoutées** :
  - `SMA_50` : Moyenne mobile à 50 périodes.
  - `Volume_Spike` : Détection des pics de volume (> 2× écart-type).

📌 *Note : Les données en temps réel nécessitent des APIs payantes.*

Les données sont extraites et stockées dans **BigQuery** pour une analyse à grande échelle.

---

## 🧠 **Sentiment du marché – `sentiment_data`**

- **Source** : **CNN Business Fear & Greed Index**.
- Indicateur du **sentiment des investisseurs** : Utilisé pour détecter les phases de **panique** ou **d’euphorie** sur le marché.

---

## 📰 **Données économiques – `news_data`**

- **Source** : Flux RSS d’actualités économiques provenant de diverses sources fiables.
- Extraction des **5 dernières nouvelles** pertinentes.
- Nettoyage et stockage des données dans **BigQuery**.
- Visualisation de l'impact des actualités économiques sur les marchés dans le **dashboard Streamlit**.

---

## 💼 **Portefeuille utilisateur – `wallet_data`**

- **Source** : Un fichier CSV (`Wallet.csv`) simulant un portefeuille d’investisseur.
- Extraction des **tickers**, des **prix d’achat**, du **prix moyen** et de la **performance**.
- Suivi visuel de chaque position dans **Streamlit**.

Les données sont extraites d'un **Bucket GCP** (Google Cloud Storage) pour être utilisées dans les calculs de performance du portefeuille.

---

## 🤖 **GRU Agent – `GruAgent.py`**

Le modèle **GRU** a été entraîné dans le notebook `IA_research.ipynb`, puis exporté sous forme de modèle `.keras` pour être utilisé dans l'application.

- 🔁 **Modèle RNN** adapté aux séries temporelles.
- ✅ Plus léger et plus rapide que LSTM, idéal pour les prévisions en temps réel.
- 🎯 Performance optimale pour la prédiction des prix sur la base des indicateurs techniques et des données de sentiment.

---

## 📊 **Visualisation – `graph.py` + Streamlit**

- **Visualisation dynamique** via **Streamlit**, permettant à l'utilisateur d'explorer les données et les prédictions de manière interactive.
- Les graphiques sont gérés par une **classe dédiée** dans `graph.py` pour une séparation claire des préoccupations.

💡 **Suggestion pour l’entreprise** : Le dashboard pourrait être migré vers des outils comme **Power BI** ou **Tableau** pour une visualisation plus poussée à grande échelle.

---

## 🚀 **Main – `main.py`**

Le fichier principal **`main.py`** est le point d'entrée du projet. Il coordonne l'exécution des pipelines et la mise à jour des données.

- Exécution automatique de tous les **pipelines** à intervalle régulier.
- Les données sont mises à jour entre **13h30 et 21h30 UTC+1** chaque jour.
- Lancement de l’application **Streamlit** pour la visualisation.

Le projet peut être déployé dans **GCP** pour une exécution continue et scalable.

---

## ✅ **Objectifs pédagogiques**

- Structuration et organisation propre d'un projet Data & IA.
- Pratique avancée des **pipelines ETL** pour le traitement et le stockage des données.
- Application de **deep learning** pour la prédiction de tendances financières.
- Création d'un **dashboard interactif** avec **Streamlit** pour la visualisation en temps réel.
