import feedparser
import pandas as pd
import pytz
from datetime import datetime
import sqlite3
import pytz
from datetime import datetime

class PipeNewsData():

    def extract(self, rss_url):
        feed = feedparser.parse(rss_url)
        if len(feed.entries) == 0:
            return "Pas de news aujourd'hui"
        else:
            return [[entry.title, entry.summary, entry.published] for entry in feed.entries]

    def transform(self, data):
        news_data = pd.DataFrame(data, columns=['Titre', 'Résumé', 'Date'])
        news_data = news_data.astype({"Titre": "string", "Résumé": "string"})
        news_data["Date"] = pd.to_datetime(news_data["Date"], format="%a, %d %b %Y %H:%M:%S %Z", errors='coerce', utc=True)
        news_data["Titre"] = news_data["Titre"].str.upper()
        news_data = news_data.rename(columns={'Date' : 'Datetime'})
        news_data = news_data.set_index('Datetime')
        news_data.index = news_data.index.tz_convert("Europe/Paris")
        news_data.index = news_data.index.strftime("%Y-%m-%d %H:%M:%S")
        return news_data
