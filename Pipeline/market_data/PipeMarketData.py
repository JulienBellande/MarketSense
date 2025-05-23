import pandas as pd
import numpy as np
import yfinance as yf
from ta.trend import SMAIndicator
import sqlite3
import pytz
from datetime import datetime

class PipeMarketData():

    def extract(self, ticker):
            market_data = yf.download(ticker, period="730d", interval="1h")
            return market_data

    def transform(self, market_data):
        market_data = market_data.droplevel(level=1, axis=1)
        market_data['SMA_50'] = SMAIndicator(close=market_data['Close'], window=50).sma_indicator()
        market_data['Volume_Spike'] = (
            market_data['Volume'] / market_data['Close'].pct_change().std()
            ).rolling(90).apply(lambda x: x.iloc[-1] > 2 * x.mean()
        )
        market_data = market_data.dropna()
        if market_data.index.tz is None:
            market_data.index = market_data.index.tz_localize("UTC")
        market_data.index = market_data.index.tz_convert("Europe/Paris")
        market_data.index = market_data.index.strftime("%Y-%m-%d %H:%M:%S")
        return market_data
