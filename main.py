import pandas as pd
import numpy as np
from Pipeline.core.main_pipeline import run_pipeline
from graph import Graph
import streamlit as st
import streamlit.components.v1 as components
from streamlit_ace import st_ace

pipeline = run_pipeline()
graph = Graph()

pipeline.run()

st.set_page_config(layout="wide")
st.title("MarketSense")
st.write("Je vous invite à voir le code des Pipeline, de l'IA et du dashboard sur mon GitHub : https://github.com/JulienBellande/MarketSense")
page = st.selectbox("Choisir une page", ["MarketSense", "IA_research", 'documentation'])

if page == "MarketSense":
    col1, col2 = st.columns([9,2])
    with col1:
        tickers = ["Nasdaq100", "SP500", "DowJones30", "Apple", "Tesla", "Google", "Amazon", "Nvidia", "Meta Platforms"]
        ticker = st.selectbox("Choisissez un Ticker", tickers)
        st.plotly_chart(graph.graph_stockmarket(ticker))
        st.caption("💡 Astuce : Vous pouvez retirer des features du graphique en cliquant sur les éléments de la légende. Cela rendra le graphique plus lisible.")
    with col2:
        news_df = graph.graph_news()
        st.subheader("📰 Dernières actualités économiques")

        for index, row in news_df.iterrows():
            with st.expander(row['Titre'], expanded=False):
                st.write("**Résumé:**", row['Résumé'])
                st.write("**Date:**", row['Datetime'])
                st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graph.graph_wallet())

    with col2:
        st.plotly_chart(graph.graph_sent())

if page == "IA_research":
    with open("IA_research.html", "r") as file:
        notebook_html = file.read()
    components.html(notebook_html, height=800)
