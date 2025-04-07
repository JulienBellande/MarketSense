import pandas as pd
import plotly.graph_objects as go
from google.cloud import bigquery
from google.oauth2 import service_account
from Model.GruAgent import GruAgent
import streamlit as st
from datetime import datetime


class Graph():
    def __init__(self):
        creds_dict = dict(st.secrets["gcp_credentials"])
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n") if "\\n" in creds_dict["private_key"] else creds_dict["private_key"]
        self.credentials = service_account.Credentials.from_service_account_info(creds_dict)
        self.project_id = creds_dict["project_id"]
        self.client = bigquery.Client(
            credentials=self.credentials,
            project=self.project_id
        )
        self.agent = GruAgent()

    def graph_stockmarket(self, ticker):
        query = f"""
                SELECT *
                FROM `{self.project_id}.Database.{ticker}`
                ORDER BY Datetime ASC"""
        df = self.client.query(query).to_dataframe()
        x = self.agent.preprocessing(df['Close'])
        x = self.agent.create_last_sequence(x)
        predict = self.agent.predict(x)

        last_date = pd.to_datetime(df["Datetime"].iloc[-1])
        predicted_date = last_date + pd.Timedelta(days=1)

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
            marker=dict(symbol="star", size=10, color="yellow",
                       line=dict(width=2, color="black")),
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
        query = f"""SELECT *
                FROM `{self.project_id}.Database.Sent_Data`"""
        df = self.client.query(query).to_dataframe()
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
                "font": {"size": 40, "color": color}
            },
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
            title="Investor sentiment",
            width=600,
            height=400,
            template="plotly_dark",
            margin=dict(t=50, b=20)
        )
        return fig

    def graph_news(self):
        query = f"""SELECT *
        FROM `{self.project_id}.Database.News_Data`
        ORDER BY Datetime DESC"""
        df = self.client.query(query).to_dataframe()
        return df.iloc[:5]

    def graph_wallet(self):
        query = f"SELECT * FROM `{self.project_id}.Database.Wallet_Data`"
        df = self.client.query(query).to_dataframe()
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
                range=[df["Return"].min() * 1.2, df["Return"].max() * 1.2],
                zeroline=True,
                zerolinecolor="gray",
            ),
            template="plotly_dark"
        )
        return fig
