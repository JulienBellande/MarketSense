# 📊 MarketSense

**MarketSense** est un projet de simulation du rôle de **Data Engineer Analytics** avec une spécialisation en **IA appliquée à la finance**.
L’objectif est de construire un **dashboard d’aide à la décision** pour des investisseurs **intraday** et **long terme**.

🧱 Le projet repose sur :
- des pipelines ETL robustes,
- le stockage de données en **SQL**,
- un modèle de réseau neuronal **GRU** pour la prédiction des marchés,
- et une application **Streamlit** pour la visualisation interactive.

L’ensemble du code est orienté objet via des **classes Python**.

---

## 🗂️ Architecture du projet

├── Database
│   └── database.db
├── GRU_Agent.keras
├── GruAgent.py
├── IA_research.ipynb
├── Pipeline
│   ├── core
│   │   ├── __pycache__
│   │   │   └── main_pipeline.cpython-310.pyc
│   │   └── main_pipeline.py
│   ├── market_data
│   │   ├── PipeMarketData.py
│   │   └── __pycache__
│   │       └── PipeMarketData.cpython-310.pyc
│   ├── news_data
│   │   ├── PipeNewsData.py
│   │   └── __pycache__
│   │       └── PipeNewsData.cpython-310.pyc
│   ├── sentiment_data
│   │   ├── PipeSentimentData.py
│   │   └── __pycache__
│   │       └── PipeSentimentData.cpython-310.pyc
│   ├── storage
│   │   ├── StorageData.py
│   │   └── __pycache__
│   │       └── StorageData.cpython-310.pyc
│   └── wallet_data
│       ├── PipeWalletData.py
│       └── __pycache__
│           └── PipeWalletData.cpython-310.pyc
├── README.md
├── Wallet.csv
├── __pycache__
│   ├── GruAgent.cpython-310.pyc
│   └── graph.cpython-310.pyc
├── graph.py

---

## 🔄 Pipelines

Les pipelines suivent les **bonnes pratiques d’entreprise** (modularité, scalabilité, maintenance).

- Extraction → Transformation → Stockage
- Toutes les données sont **uniformisées** (horaires européens).
- Les bases SQL sont **rafraîchies à chaque exécution** (dans ce prototype).
  En production, elles seraient **alimentées en continu**.

---

## 📈 Données des marchés financiers – `market_data`

Source : **Yahoo Finance** via l’API `yfinance`.

- Données horaires du marché américain
- Prix : Open, High, Low, Close de l’heure précédente
- **Features ajoutées :**
  - `SMA_50` : Moyenne mobile 50 périodes
  - `Volume_Spike` : Pic de volume anormal (> 2× écart-type)

📌 *Les données temps réel nécessitent des APIs payantes.*

---

## 🧠 Sentiment du marché – `sentiment_data`

Source : **CNN Business Fear & Greed Index**

- Indicateur global du **sentiment des investisseurs**
- Très utile pour détecter les phases de **panique ou d’euphorie**

---

## 📰 Données économiques – `news_data`

Source : **flux RSS d’actualités économiques**

- Récupération des 5 dernières news
- Stockage et nettoyage via SQL
- Visualisation intégrée dans le dashboard

---

## 💼 Portefeuille utilisateur – `wallet_data`

Source : un fichier CSV (`Wallet.csv`) simulant les positions d’un investisseur.

- Extraction des tickers et prix d’achat
- Calcul du **prix moyen** et de la **performance (%)**
- Suivi visuel de chaque position sur Streamlit

---

## 🤖 GRU Agent – `GruAgent.py`

Le modèle GRU a été entraîné dans `IA_research.ipynb` puis exporté (`GRU_Agent.keras`) pour être utilisé dans l’application.

- 🔁 Modèle RNN adapté aux séries temporelles
- ✅ Plus léger et plus rapide que LSTM
- 🎯 Excellente performance pour la prédiction temps réel

---

## 📊 Visualisation – `graph.py` + Streamlit

- Visualisation dynamique sur **Streamlit**
- Les graphes sont gérés via une **classe dédiée** dans `graph.py` pour plus de lisibilité

💡 En entreprise, le dashboard pourrait être migré vers **Power BI** ou **Tableau**.

---

## 🚀 Main – `main.py`

C’est le point d’entrée du projet :

- Exécute tous les **pipelines**
- Met à jour automatiquement les données toutes les heures entre **13h30 et 21h30 (UTC+1)**
- Lance l’application Streamlit

---

## ✅ Objectifs pédagogiques

- Structuration propre d’un projet Data & IA
- Pratique avancée des **pipelines ETL**
- Application concrète du **deep learning** en finance
- Déploiement d’un **dashboard interactif**

---

## 🛠️ À venir

- Connexion en **temps réel** via WebSockets ou APIs premium
- Déploiement **Cloud (GCP/AWS)** du dashboard Streamlit
- Enrichissement du modèle (multi-actifs, NLP des news, etc.)

---
