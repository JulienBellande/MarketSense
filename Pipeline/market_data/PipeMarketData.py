import pandas as pd
import numpy as np
import yfinance as yf
import talib
import sqlite3
import pytz
from datetime import datetime

class PipeMarketData():

    def extract(self, ticker):
            market_data = yf.download(ticker, period="730d", interval="1h")
            return market_data

    def transform(self, market_data):
        market_data = market_data.droplevel(level=1, axis=1)
        market_data['Volume'] = market_data['Volume'].mask(market_data['Volume'] == 0).ffill()
        market_data['Return'] = market_data['Close'].pct_change(45)*100
        market_data["SMA"] = talib.SMA(market_data["Close"], timeperiod=45)
        market_data["RSI"] = talib.RSI(market_data["Close"], timeperiod=45)
        market_data['High_Volume_Zone'] = (
            market_data['Volume'] / market_data['Return'].std()
            ).rolling(45).apply(lambda x: x.iloc[-1] > 2 * x.mean()
        )
        market_data = market_data.dropna()
        if market_data.index.tz is None:
            market_data.index = market_data.index.tz_localize("UTC")
        market_data.index = market_data.index.tz_convert("Europe/Paris")
        market_data.index = market_data.index.strftime("%Y-%m-%d %H:%M:%S")
        return market_data
