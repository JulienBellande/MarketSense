import pandas as pd
import os
from Pipeline.market_data.PipeMarketData import PipeMarketData
from Pipeline.news_data.PipeNewsData import PipeNewsData
from Pipeline.sentiment_data.PipeSentimentData import PipeSentimentData
from Pipeline.wallet_data.PipeWalletData import PipeWalletData
from Pipeline.storage.StorageData import StorageData


class run_pipeline():

    def __init__(self):
        self.web_url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        self.rss_url = "https://www.ft.com/rss/home"
        self.wallet_path = "/Users/julienbellande/code/JulienBellande/MarketSense/Wallet.csv"

        self.tickers = {
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

        self.storage = StorageData()
        self.pipemarketdata = PipeMarketData()
        self.pipenewsdata = PipeNewsData()
        self.pipesentdata = PipeSentimentData()
        self.pipewalletdata = PipeWalletData()

    def run(self):

        list_news = self.pipenewsdata.extract(self.rss_url)
        news_data = self.pipenewsdata.transform(list_news)
        self.storage.store(news_data, table_name='News_Data')

        sent_data = self.pipesentdata.extract(self.web_url)
        sent_data = self.pipesentdata.transform(sent_data)
        self.storage.store(sent_data, table_name='Sent_Data')

        for ticker in self.tickers.keys():
            market_data = self.pipemarketdata.extract(ticker)
            market_data = self.pipemarketdata.transform(market_data)
            self.storage.store(market_data, table_name=f'{self.tickers[ticker]}')

        wallet_data = self.pipewalletdata.extract(self.wallet_path)
        wallet_data = self.pipewalletdata.transform(wallet_data)
        self.storage.store(wallet_data, table_name='Wallet_data')
