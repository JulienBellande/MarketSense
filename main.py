import pandas as pd
import numpy as np
from Pipeline.core.main_pipeline import Pipeline
from Graph.graph import Graph
import yfinance as yf
import streamlit as st
import streamlit.components.v1 as components
from nbconvert import HTMLExporter
from datetime import datetime
import time as
from streamlit_ace import st_ace
from nbformat import read

st.set_page_config(layout="wide")

graph = Graph()
pipeline = Pipeline()

st.title("MarketSense")
st.write("Voir le code sur GitHub : https://github.com/JulienBellande/MarketSense")


pipeline.run()

page = st.selectbox("Choisir une page", ["MarketSense", "MarketSense: IA_research", "MarketSense: Documentation"])

if page == "MarketSense":
    col1, col2 = st.columns([9, 2])
    with col1:
        tickers = ["Nasdaq100", "SP500", "DowJones30", "Apple", "Tesla",
                  "Google", "Amazon", "Nvidia", "Meta"]
        ticker = st.selectbox("Choisissez un Ticker", tickers)
        st.plotly_chart(graph.graph_stockmarket(ticker), use_container_width=True)
        st.caption("💡 Astuce : Cliquez sur les éléments de la légende pour filtrer.")
    with col2:
        st.subheader("📰 Dernières actualités")
        news_df = graph.graph_news()
        for _, row in news_df.iterrows():
            with st.expander(row['Titre']):
                st.write(f"**Résumé:** {row['Résumé']}")
                st.write(f"**Date:** {row['Datetime']}")
                st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graph.graph_wallet(), use_container_width=True)
    with col2:
        st.plotly_chart(graph.graph_sent(), use_container_width=True)

elif page == "MarketSense: IA_research":
    notebook = read(open("IA_research.ipynb", encoding='utf-8'), as_version=4)
    st.components.v1.html(HTMLExporter().from_notebook_node(notebook)[0],
                         height=5000, scrolling=True)

elif page == "MarketSense: Documentation":
    notebook = read(open("Documentation.ipynb", encoding='utf-8'), as_version=4)
    st.components.v1.html(HTMLExporter().from_notebook_node(notebook)[0],
                         height=5000, scrolling=True)
