import seaborn as sns
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import sqlite3
import plotly.express as px
from GruAgent import GruAgent


class Graph():

    def __init__(self):
        self.conn = sqlite3.connect("Database/database.db")
        self.agent = GruAgent()

    def graph_stockmarket(self, ticker):
        df = pd.read_sql_query(f"SELECT * FROM {ticker}", self.conn)
        x = self.agent.preprocessing(df['Close'])
        x = self.agent.create_last_sequence(x)
        predict = self.agent.predict(x)
        last_date = pd.to_datetime(df["Datetime"].iloc[-1])
        predicted_date = last_date + pd.Timedelta(days=1)
        df = df.dropna()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["Datetime"],
            y=df["Close"],
            name="Price",
            line=dict(color="blue", width=2)
        ))

        fig.add_trace(go.Scatter(
            x=df["Datetime"],
            y=df["SMA_50"],
            mode="lines",
            name="SMA 50",
            line=dict(color="red", width=2)
        ))

        fig.add_trace(go.Scatter(
            x=[predicted_date],
            y=[predict],
            mode="markers",
            name="Prédiction",
            marker=dict(symbol="star", size=10, color="yellow", line=dict(width=2, color="black")),
            showlegend=True
        ))

        spike_data = df[df["Volume_Spike"] == 1.0]
        fig.add_trace(go.Scatter(
            x=spike_data["Datetime"],
            y=spike_data["High"],
            mode="markers",
            name="Volume Spike",
            marker=dict(size=8, color="purple", symbol="circle"),
            showlegend=True
        ))

        fig.update_layout(
            xaxis_rangeslider_visible=False,
            title=f"{ticker}",
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode="x unified",
            width=1500,
            height=500,
            showlegend=True
        )
        return fig

    def graph_sent(self):
        df = pd.read_sql_query("SELECT * FROM Sent_Data", self.conn)
        df["Datetime"] = pd.to_datetime(df["Datetime"])

        rating_colors = {
            "Extreme Fear": "#8B0000",
            "Fear": "#FF0000",
            "Neutral": "#808080",
            "Greed": "#228B22",
            "Extreme Greed": "#006400"
        }

        sentiment = df.loc[0, "rating"]
        score = df.loc[0, "score"]
        color = rating_colors.get(sentiment, "gray")


        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={
            "suffix": "/100",
            "font": {
                "size": 40,
                "color": color
                } },
            title={"text": f"Sentiment : {sentiment}", "font": {"size": 14}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 20], "color": "#8B0000"},
                    {"range": [20, 40], "color": "#FF0000"},
                    {"range": [40, 60], "color": "#808080"},
                    {"range": [60, 80], "color": "#228B22"},
                    {"range": [80, 100], "color": "#006400"},
                ]
            }
        ))

        fig.update_layout(
            title ="Investor sentiment",
            width=600,
            height=400,
            template="plotly_dark",
            margin=dict(t=50, b=20)
        )

        return fig


    def graph_news(self):
        df = pd.read_sql_query(f"SELECT * FROM News_Data", self.conn)
        df = df.sort_values('Datetime')
        news = df.iloc[-5:]
        return news

    def graph_wallet(self):
        df = pd.read_sql_query(f"SELECT * FROM Wallet_Data", self.conn)
        df = df[['Ticker', 'Return']]
        colors = ["red" if x < 0 else "green" for x in df["Return"]]
        fig = go.Figure(go.Bar(
            x=df["Return"],
            y=df["Ticker"],
            marker_color=colors,
            text=[f"{x:.2f}%" for x in df["Return"]],
            textposition="outside",
            orientation="h"
        ))
        fig.update_layout(
            title="Wallet",
            width=600,
            height=400,
            xaxis_title="Return (%)",
            yaxis_title="Ticker",
            xaxis=dict(
                range=[df["Return"].min() * 1.2, df["Return"].max()* 1.2],
                zeroline=True,
                zerolinecolor="gray",
            ),
            template="plotly_dark"
        )
        return fig
