import requests
import pytz
import pandas as pd
import numpy as np
import sqlite3
import requests
from datetime import datetime
import pytz



class PipeSentimentData():

    def extract(self, web_url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
        }
        response = requests.get(web_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
        return data

    def transform(self, data):
        sent_data = pd.DataFrame([data["fear_and_greed"]])
        local_timezone = pytz.timezone("Europe/Paris")
        sent_data['timestamp'] = pd.to_datetime(sent_data['timestamp'], utc=True)
        sent_data['timestamp'] = sent_data['timestamp'].dt.tz_convert(local_timezone)
        sent_data = sent_data.rename(columns={'timestamp': 'Datetime'})
        sent_data['Datetime'] = sent_data['Datetime'].dt.strftime("%Y-%m-%d %H:%M:%S")
        sent_data['rating'] = sent_data['rating'].apply(lambda x: x.title())
        sent_data = sent_data.set_index('Datetime')
        return sent_data
