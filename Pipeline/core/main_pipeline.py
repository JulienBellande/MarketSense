import pandas as pd
import os
from Pipeline.market_data.PipeMarketData import PipeMarketData
from Pipeline.news_data.PipeNewsData import PipeNewsData
from Pipeline.sentiment_data.PipeSentimentData import PipeSentimentData
from Pipeline.wallet_data.PipeWalletData import PipeWalletData
from Pipeline.storage.StorageData import StorageData

web_url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
rss_url = "https://www.ft.com/rss/home"
wallet_path = "/Users/julienbellande/code/JulienBellande/MarketSense/Wallet.csv"

tickers = {
    "^IXIC": "Nasdaq100",
    "^GSPC": "SP500",
    "^DJI": "DowJones30",
    "AAPL" : "Apple",
    "TSLA" : "Tesla",
    "GOOGL" : "Google",
    "AMZN" : "Amazon",
    "NVDA" : "Nvidia",
    "META" : "Meta Platforms",
    }

storage = StorageData()
pipemarketdata = PipeMarketData()
pipenewsdata = PipeNewsData()
pipesentdata = PipeSentimentData()
pipewalletdata = PipeWalletData()

list_news = pipenewsdata.extract(rss_url)
news_data = pipenewsdata.transform(list_news)
storage.store(news_data, table_name='News_Data')

sent_data = pipesentdata.extract(web_url)
sent_data = pipesentdata.transform(sent_data)
storage.store(sent_data, table_name='Sent_Data')

for ticker in tickers.keys():
    market_data = pipemarketdata.extract(ticker)
    market_data = pipemarketdata.transform(market_data)
    storage.store(market_data, table_name=f'{tickers[ticker]}')

wallet_data = pipewalletdata.extract(wallet_path)
wallet_data = pipewalletdata.transform(wallet_data)
storage.store(wallet_data, table_name='Wallet_data')
